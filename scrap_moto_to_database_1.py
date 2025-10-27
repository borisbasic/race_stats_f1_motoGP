import os
import time
import requests
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

all_races = pd.read_csv('/home/boris/Documents/matplotlib_exercize/moto_pdfs/motogp/races_2025.csv')
op = webdriver.FirefoxOptions()
op.add_argument("--headless")
for ind, row in all_races.iterrows():
    ses = '2025'
    race = row['race']
    race_small = row['race_small']
    list_of_races = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/moto2/{ses}')
    if race in list_of_races:
        continue
    else:
        os.mkdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/moto2/{ses}/{race}')
    url = f'https://www.motogp.com/en/gp-results/{ses}/{race_small}/moto2/rac/classification'
    if not os.path.exists(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/moto2/{ses}'):
        os.mkdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/moto2/{ses}')
    driver = webdriver.Firefox(options=op)
    driver.get(url)
    try:
        btn =  WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.ID, 'onetrust-pc-btn-handler')))
        btn.click()
        time.sleep(3)
        confirm = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ot-btn-container')))
        confirm_button = WebDriverWait(confirm[0], 10).until(EC.presence_of_all_elements_located(
            (By.TAG_NAME, 'button')))

        confirm_button[1].click()
    except:
        pass

    shifts = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, 'primary-filter__filter-container')))
    races = shifts[2]

    dict_races = {
        'races': [],
        'session': []
    }
    session = shifts[4]
    opt = WebDriverWait(session, 10).until(EC.presence_of_all_elements_located(
        (By.TAG_NAME, 'option')))
    for o in opt:
        dict_races['session'].append((o.get_attribute('value'), o.text))

    for s in dict_races['session']:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(f'https://www.motogp.com/en/gp-results/{ses}/{race_small}/moto2/{s[0]}/classification')
        try:
            pdfs_cont = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
                (By.CLASS_NAME, 'pdf-table__container')))
        except:
            driver.close()
            continue
        btns = WebDriverWait(pdfs_cont[0], 10).until(EC.presence_of_all_elements_located(
            (By.TAG_NAME, 'button')))
        
        os.mkdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/moto2/{ses}/{race}/{s[0]}')
        list_of_folders = ['session_results', 'championship_results', 'event_results']
        i = 0
        pdfs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'pdf-table__table-row')))
        for p in pdfs:
            req = requests.get(p.get_attribute('href'), stream=True)
            name_file = p.get_attribute('href').split('?')[0].split('/')[-1]
            with open(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/moto2/{ses}/{race}/{s[0]}/{name_file}', 'wb') as file:
                file.write(req.content)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    driver.close()