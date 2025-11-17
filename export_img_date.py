import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
from statistics import mean
from sqlalchemy import create_engine, Table, MetaData, select, and_, insert
from datetime import datetime
engine = create_engine("mariadb+mariadbconnector://root:boris123@localhost:3306/motogp")
metadata = MetaData()
circuit_info = Table(
    'circuit_info',
    metadata,
    autoload_with=engine,
    autoload_replace=True
)
races_all = Table(
    'races',
    metadata,
    autoload_with=engine,
    autoload_replace=True
)
sns.set_theme()
plt.style.use('ggplot')

class_moto = os.listdir('/home/boris/Documents/matplotlib_exercize/moto_pdfs')

images_moto = '/home/boris/Documents/motogp_api/images'

for cm in class_moto:
    important_things_csv = '/home/boris/Documents/matplotlib_exercize/done/img_date.csv'
    important_things_csv = pd.read_csv(important_things_csv)
    important_races = important_things_csv['race'].tolist()
    important_years = important_things_csv['year'].tolist()
    important_classes = important_things_csv['class'].tolist()
    important_done = important_things_csv['is_done'].tolist()
    if cm not in ['motogp', 'moto2', 'moto3']:
        continue
    year = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}')
    for y in year:
        if y not in ['2025']:#'2019', '2020', '2021', '2022', '2023', '2024']:
            continue
        list_of_year = os.listdir(f'{images_moto}/{cm}')
        if y not in list_of_year:
            os.mkdir(f'{images_moto}/{cm}/{y}')
        if not os.path.isdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}'):
            continue
        races = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}') 
        for r in races:
            dones = important_things_csv[(important_things_csv['race'] == r) & (important_things_csv['year'] == int(y)) & (important_things_csv['class'] == cm)]['is_done'].tolist()
            
            if 'yes' in dones:
                continue
            list_of_races = os.listdir(f'{images_moto}/{cm}/{y}')
            important_races.append(r)
            important_years.append(y)
            important_classes.append(cm)
            if r not in list_of_races:
                os.mkdir(f'{images_moto}/{cm}/{y}/{r}')
            seasion = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}')
            for s in seasion:
                if s not in ['rac']:
                    continue

                race_import = select(races_all).where(and_(races_all.c.race == r,
                                                    races_all.c.year == int(y)))
                with engine.connect() as conn:
                    result = conn.execute(race_import).fetchone()
                    result_id = result.id
                    
                list_of_seasion = os.listdir(f'{images_moto}/{cm}/{y}/{r}')
                if s not in list_of_seasion:
                    os.mkdir(f'{images_moto}/{cm}/{y}/{r}/{s}')
                pdf_patg_final_results = f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/CircuitInformation.pdf'
                try:
                    with pdfplumber.open(pdf_patg_final_results) as pdf:
                        page = pdf.pages[0]
                        page_width = page.width
                        page_height = page.height
                        bbox = (470, 27, 580, 125)
                        bbox2 = (40, 350, 320, 495)
                        cropped = page.crop(bbox).to_image(resolution=150)
                        cropped.save(f"{images_moto}/{cm}/{y}/{r}/{s}/circuit_small_page.png", format="PNG")

                        cropped = page.crop(bbox2).to_image(resolution=150)
                        cropped.save(f"{images_moto}/{cm}/{y}/{r}/{s}/circuit_big_page.png", format="PNG")
                except: 
                    continue
                with pdfplumber.open(pdf_patg_final_results) as pdf:
                    page = pdf.pages[0]
                    page_width = page.width
                    page_height = page.height
                    crop_box_1 = (20, 800, 350, 840)
                    date = page.within_bbox(crop_box_1).extract_text()
                    date = ', '.join(date.split(', ')[2:])
                    crop_box_1 = (0, 70, page_width-120, 105)
                    info = page.within_bbox(crop_box_1).extract_text()
                    name = info.split('\n')[1]
                    infos = info.split('\n')[0].split(':')[1:][0].strip()
                    dict_info = {
                        'name': name,
                        'date': date,
                        'info': infos
                    }

                    insert_info = insert(circuit_info).values(name=name,
                                                               info=infos,
                                                               date=datetime.strptime(date, "%B %d, %Y").date(),
                                                               race_id=result_id)
                    with engine.connect() as conn:
                        conn.execute(insert_info)
                        conn.commit()

                    df = pd.DataFrame([dict_info])
                    df.to_csv(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/circuit_info.csv', index=False)
                #except:
                #    continue

            important_done.append('yes')
            new_dict = {'race': important_races, 
                        'is_done': important_done, 
                        'year': important_years, 
                        'class': important_classes}
            new_df = pd.DataFrame(new_dict)
            new_df.to_csv('/home/boris/Documents/matplotlib_exercize/done/img_date.csv', index=False)