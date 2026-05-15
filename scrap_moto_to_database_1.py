import os
import time
import pandas as pd
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine, insert, Table, MetaData, select, and_

# 1. KONFIGURACIJA URLLIB-a
# Pravimo opener koji simulira pravi browser i šalje Referer
opener = urllib.request.build_opener()
opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'),
    ('Referer', 'https://www.motogp.com/')
]
urllib.request.install_opener(opener)

# Database setup
engine = create_engine("mariadb+mariadbconnector://root:boris123@localhost:3306/motogp")
engine_n = create_engine(f"mariadb+mariadbconnector://motogpuser:3TEA8Tohoy6iwLbDVYEL@23.95.167.114:3306/motogp")
metadata = MetaData()
races_table = Table('races', metadata, autoload_with=engine)

all_races = pd.read_csv('/home/boris/Documents/matplotlib_exercize/moto_pdfs/motogp/races_2026.csv')

# Pokrećemo driver
op = webdriver.FirefoxOptions()
op.add_argument("--headless")
driver = webdriver.Firefox()#options=op)

for ind, row in all_races.iterrows():
    ses = '2026'
    race = row['race']
    race_small = row['race_small']
    
    # Putanja za Moto2
    base_dir = f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/moto2/{ses}/{race}'
    os.makedirs(base_dir, exist_ok=True)
    check_path = f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/motogp/{ses}/{race}/rac/Analysis.pdf'
    if os.path.exists(check_path):
        continue
    # Database provera i unos
    with engine.connect() as conn:
        query = select(races_table).where(and_(
            races_table.c.race == race,
            races_table.c.race_small == race_small,
            races_table.c.year == int(ses)
        ))
        result = conn.execute(query).fetchone()
        if result is None:
            conn.execute(insert(races_table).values(race=race, race_small=race_small, year=int(ses)))
            conn.commit()
            with engine_n.connect() as conn_n:
                conn_n.execute(insert(races_table).values(race=race, race_small=race_small, year=int(ses)))
                conn_n.commit()
    

    url = f'https://www.motogp.com/en/gp-results/{ses}/{race_small}/moto2/rac/classification'
    driver.get(url)

    # Prihvatanje kolačića
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))).click()
        time.sleep(2)
    except:
        pass

    # Dohvatanje sesija (P1, P2, RAC...)
    try:
        shifts = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'primary-filter__filter-container')))
        session_filter = shifts[4]
        options = session_filter.find_elements(By.TAG_NAME, 'option')
        session_list = [(o.get_attribute('value'), o.text) for o in options]
    except Exception as e:
        print(f"Nema filtera sesija za {race}: {e}")
        continue

    for s_val, s_text in session_list:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(f'https://www.motogp.com/en/gp-results/{ses}/{race_small}/moto2/{s_val}/classification')

        session_dir = os.path.join(base_dir, s_val)
        os.makedirs(session_dir, exist_ok=True)

        try:
            # Čekamo da se pojave redovi sa PDF-ovima
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'pdf-table__table-row')))
            
            # Mala pauza da JS popuni href atribute
            time.sleep(1)
            
            pdf_elements = driver.find_elements(By.CLASS_NAME, 'pdf-table__table-row')
            # Uzimamo URL-ove odmah da izbegnemo StaleElement greške
            links = [p.get_attribute('href') for p in pdf_elements if p.get_attribute('href')]
            
            for pdf_url in links:
                file_name = pdf_url.split('?')[0].split('/')[-1]
                file_path = os.path.join(session_dir, file_name)
                
                # Provera da li fajl već postoji i da li je validan
                if os.path.exists(file_path) and os.path.getsize(file_path) > 2000:
                    continue

                print(f"Skidam preko urllib: {file_name} za {s_text}...")
                
                try:
                    # Direktan download preko urllib
                    urllib.request.urlretrieve(pdf_url, file_path)
                    
                    # Posebna provera za Entry list ili male fajlove
                    if os.path.getsize(file_path) < 1000:
                        print(f"Upozorenje: {file_name} je sumnjivo mali, ponavljam...")
                        time.sleep(2)
                        urllib.request.urlretrieve(pdf_url, file_path)
                except Exception as e:
                    print(f"Greška pri downloadu {file_name}: {e}")
                    
        except Exception as e:
            print(f"Nema PDF tabele za sesiju {s_text}")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

driver.quit()
print("Moto2 obrada završena.")

import transfer_images
transfer_images.deploy()