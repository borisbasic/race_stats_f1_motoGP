import shutil
import os
import pandas as pd
images_moto = '/home/boris/Documents/motogp_api/images'
class_moto = os.listdir('/home/boris/Documents/matplotlib_exercize/moto_pdfs')

all_races = pd.read_csv('/home/boris/Documents/matplotlib_exercize/moto_pdfs/motogp/races_2025.csv')
#op = webdriver.FirefoxOptions()
#op.add_argument("--headless")
for ind, row in all_races.iterrows():
    ses = '2025'
    race = row['race']
    race_small = row['race_small']
    print(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/motogp/{ses}/{race}/rac/Anaylsis.pdf')
    list_of_races = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/moto2/{ses}')
    if not os.path.exists(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/moto2/{ses}/{race}'):
        os.mkdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/moto2/{ses}/{race}')
    if os.path.exists(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/motogp/{ses}/{race}/rac/Analysis.pdf'):
        print('File exists, skipping...')
        continue