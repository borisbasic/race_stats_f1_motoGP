import os
import time
import pandas as pd
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. KONFIGURACIJA URLLIB OPENER-A (Ovo se radi jednom na početku)
opener = urllib.request.build_opener()
opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'),
    ('Referer', 'https://www.motogp.com/')
]
urllib.request.install_opener(opener)

all_races = pd.read_csv('/home/boris/Documents/matplotlib_exercize/moto_pdfs/motogp/races_2026.csv')
op = webdriver.FirefoxOptions()
op.add_argument("--headless")

for ind, row in all_races.iterrows():
    ses = '2026'
    race = row['race']
    race_small = row['race_small']
    
    # Putanja do foldera za trku
    race_dir = f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/moto3/{ses}/{race}'
    os.makedirs(race_dir, exist_ok=True)

    # Provera da li već postoji Analysis.pdf (preskačemo ako je gotovo)
    # Putanja je ovde ostala motogp kao u tvom originalu, proveri da li treba moto3
    check_path = f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/motogp/{ses}/{race}/rac/Analysis.pdf'
    if os.path.exists(check_path):
        continue

    url = f'https://www.motogp.com/en/gp-results/{ses}/{race_small}/moto3/rac/classification'
    driver = webdriver.Firefox()#options=op)
    driver.get(url)

    # Cookie Bypass
    try:
        btn = WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
        btn.click()
        time.sleep(2)
    except:
        pass

    try:
        # Pronalaženje filtera za sesije
        shifts = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'primary-filter__filter-container')))
        session_filter = shifts[4]
        options = session_filter.find_elements(By.TAG_NAME, 'option')
        session_data = [(o.get_attribute('value'), o.text) for o in options]
    except Exception as e:
        print(f"Greška pri dohvatanju sesija za {race}: {e}")
        driver.quit()
        continue

    for s_val, s_text in session_data:
        # Otvaranje svake sesije u novom tabu
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(f'https://www.motogp.com/en/gp-results/{ses}/{race_small}/moto3/{s_val}/classification')

        # Kreiranje foldera za sesiju (npr. RAC, P1, P2...)
        session_dir = os.path.join(race_dir, s_val)
        os.makedirs(session_dir, exist_ok=True)

        try:
            # Čekamo PDF tabelu da se pojavi
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'pdf-table__table-row')))
            
            # Uzimamo sve href linkove odmah
            pdf_elements = driver.find_elements(By.CLASS_NAME, 'pdf-table__table-row')
            links = [el.get_attribute('href') for el in pdf_elements if el.get_attribute('href')]

            for pdf_url in links:
                name_file = pdf_url.split('?')[0].split('/')[-1]
                full_path = os.path.join(session_dir, name_file)

                if os.path.exists(full_path) and os.path.getsize(full_path) > 2000:
                    continue

                print(f"Skidam preko urllib: {name_file} ({s_text})")
                
                # URLLIB DOWNLOAD
                try:
                    urllib.request.urlretrieve(pdf_url, full_path)
                    
                    # Provera da li je Entry.pdf skinut kako treba (ako je manji od 2KB, verovatno je greška)
                    if "Entry.pdf" in name_file and os.path.getsize(full_path) < 2000:
                        print(f"Ponovni pokušaj za {name_file}...")
                        time.sleep(2)
                        urllib.request.urlretrieve(pdf_url, full_path)
                except Exception as download_error:
                    print(f"Greška pri skidanju {name_file}: {download_error}")

        except Exception as e:
            print(f"Nema PDF-ova za sesiju {s_text}")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    driver.quit()
