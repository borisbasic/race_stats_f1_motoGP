import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
sns.set_theme()
plt.style.use('ggplot')

class_moto = os.listdir('/home/boris/Documents/matplotlib_exercize/moto_pdfs')
images_moto = '/home/boris/Documents/motogp_api/images'

for cm in class_moto:
    important_things_csv = '/home/boris/Documents/matplotlib_exercize/done/important_things.csv'
    important_things_csv = pd.read_csv(important_things_csv)
    important_races = important_things_csv['race'].tolist()
    important_years = important_things_csv['year'].tolist()
    important_classes = important_things_csv['class'].tolist()
    important_done = important_things_csv['is_done'].tolist()
    if cm not in ['motogp', 'moto2', 'moto3']:
        continue
    year = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}')
    for y in year:
        if y != '2025':
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
            if r not in list_of_races:
                os.mkdir(f'{images_moto}/{cm}/{y}/{r}')
            important_races.append(r)
            important_years.append(y)
            important_classes.append(cm)
            seasion = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}')
            for s in seasion:
                
                list_of_seasion = os.listdir(f'{images_moto}/{cm}/{y}/{r}')
                if s not in list_of_seasion:
                    os.mkdir(f'{images_moto}/{cm}/{y}/{r}/{s}')
                pdf_patg_final_results = f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/Entry.pdf'
                try:
                    with pdfplumber.open(pdf_patg_final_results) as pdf:
                        page = pdf.pages[0]
                        page_width = page.width
                        page_height = page.height
                        crop_box_1 = (80, 154, page_width, page_height-200)
                        text = page.within_bbox(crop_box_1).extract_text()
                    text = text.split('\n')
                    text_import = []
                    for t in text:
                        if '(' in t and ')' in t:
                            text_import.append(t)
                
                    text_dict = {
                        'number': [],
                        'rider': [],
                        'nickname': [],
                        'country': [],
                        'team': [],
                        'bike': [],
                        'rider_name': [],
                        'rider_surname': []
                    }

                    for ti in text_import:
                        text_dict['number'].append(ti.split(' ')[0])
                        text_dict['rider'].append(' '.join(ti.split('(')[0].split(' ')[1:]))
                        text_dict['nickname'].append(ti.split('(')[1].split(')')[0])
                        text_dict['country'].append(ti.split(')')[1].split(' ')[1])
                        last = ti.split(' ')[-1]
                        len_last = len(last) +1 
                        text_dict['team'].append((ti.split(')')[1][4:-len_last]))
                        text_dict['bike'].append(last)
                        text_dict['rider_surname'].append(' '.join(ti.split('(')[0].split(' ')[1:-2]))
                        text_dict['rider_name'].append(ti.split('(')[0].split(' ')[-2])
                    
                    df = pd.DataFrame(text_dict)
                    df.to_csv(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/entry.csv', index=False)
                except:
                    continue

            important_done.append('yes')
            new_dict = {'race': important_races, 
                        'is_done': important_done, 
                        'year': important_years, 
                        'class': important_classes}
            new_df = pd.DataFrame(new_dict)
            new_df.to_csv('/home/boris/Documents/matplotlib_exercize/done/important_things.csv', index=False)
