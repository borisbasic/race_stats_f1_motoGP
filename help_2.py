import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
from sqlalchemy import create_engine, insert, Table, MetaData, select, and_
from datetime import datetime

def clear_speed(s):
    s1 = ''
    for i in range(len(s)):
        if s[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
            s1 = s1 + s[i]
    if s1 == '':
        return 0.0
    return float(s1)

def tyre_to_num(s):
    a = 0
    b = 0
    if b < 5:
        b = 0
    else:
        b = 1
    for s1 in s:
        if s1 == 'Tyre':
            a += 1
    return (a, b)

def get_tyre(s):
    s = s.replace('Tyre', '')
    if s == 'Slick-Soft':
        return 'ss'
    elif s == 'Slick-Medium':
        return 'sm'
    elif s == 'Slick-Hard':
        return 'sh'
    elif s == 'Wet-Medium':
        return 'wm'
    elif s == 'Wet-Soft':
        return 'ws'

engine = create_engine("mariadb+mariadbconnector://root:boris123@localhost:3306/motogp")
metadata = MetaData()

races_all = Table(
    'races',
    metadata,
    autoload_with=engine,
    autoload_replace=True
)

entries_all = Table(
    'entries',
    metadata,
    autoload_with=engine,
    autoload_replace=True
)

bikes = Table(
    'bikes',
    metadata,
    autoload_replace=True,
    autoload_with=engine
)
sns.set_theme()
plt.style.use('ggplot')

class_moto = os.listdir('/home/boris/Documents/matplotlib_exercize/moto_pdfs')
ft = 'n/a'
rt = 'n/a'

images_moto = '/home/boris/Documents/motogp_api/images'
for cm in class_moto:
    if cm not in ['motogp']:
        continue
    year = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}')
    for y in year:
        if y not in ['2025']:
            continue
        list_of_year = os.listdir(f'{images_moto}/{cm}')
        if y not in list_of_year:
            os.mkdir(f'{images_moto}/{cm}/{y}')
        if not os.path.isdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}'):
            continue
        races = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}') 
        for r in races:
            #if r not in ['GRAN PREMIO DI SAN MARINO E DELLA RIVIERA DI RIMINI']:
            #    continue
            print(r)
            list_of_races = os.listdir(f'{images_moto}/{cm}/{y}')
            race_id = select(races_all.c.id).where(and_(races_all.c.race == r, races_all.c.year == int(y),))
            with engine.connect() as conn:  
                race_id = conn.execute(race_id).fetchone()[0]
            
            if r not in list_of_races:
                os.mkdir(f'{images_moto}/{cm}/{y}/{r}')
            seasion = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}')
            for s in seasion:
                #if s not  in ['wup']:
                #    continue
                print(s)
                
                #if 'yes' in dones:
                #    continue
                list_of_seasion = os.listdir(f'{images_moto}/{cm}/{y}/{r}')
                if s not in list_of_seasion:
                    os.mkdir(f'{images_moto}/{cm}/{y}/{r}/{s}')
                try:
                    drivers = pd.read_csv(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/entry.csv')
                    
                except:
                    continue
                for i, row in drivers.iterrows():
                    if row['rider_surname'] == 'RUEDA Jose':
                        drivers.at[i, 'driver_name'] = row['rider_surname'].split(' ')[1] + ' ' + row['rider_name'] + ' ' + row['rider_surname'].split(' ')[0]
                    else:
                        drivers.at[i, 'driver_name'] = row['rider_name'] + ' ' + row['rider_surname']
                drivers_n = drivers.copy()
                drivers = drivers['driver_name'].to_list()
                new_drivers = drivers

                def crop_and_extract_text(pdf_path):
                    if year == '2025' or year == '2026':
                        shift = 5
                    else:
                        shift = 20
                    with pdfplumber.open(pdf_path) as pdf:
                        all = ''
                        for page in pdf.pages:
                            first_page = page
                            page_width = first_page.width
                            page_height = first_page.height

                            crop_box = (0, 0, page_width / 2 + 5, page_height - 112)
                            cropped_page = first_page.within_bbox(crop_box)

                            crop_box_ = (page_width / 2 + 5, 0, page_width, page_height - 112)
                            cropped_page_ = first_page.within_bbox(crop_box_) 
                            text = cropped_page.extract_text()
                            text_ = cropped_page_.extract_text()
                            all = all + text + text_
                    return all

                pdf_path = f"/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/Analysis.pdf"
                try:
                    text = crop_and_extract_text(pdf_path)
                except:
                    continue
                all_text = text.split('\n')
                driver_dict = {'driver_name': [],
                            'time': [],}
                all_data = []
                def to_miliseconds(time):
                    new_time = ''
                    for t in time:
                        if t in '0123456789:.':
                            new_time = new_time + t
                    time = new_time
                    if len(time)>6:
                        try:
                            minutes = int(time.split(':')[0])*60000
                            seconds = int(time.split(':')[1].split('.')[0])*1000
                            miliseconds = int(time.split('.')[1])
                            return (minutes+seconds+miliseconds)/1000
                        except:
                            return ''
                    else:
                        try:
                            seconds = int(time.split('.')[0])*1000
                            miliseconds = int(time.split('.')[1])
                            return (seconds+miliseconds)/1000
                        except:
                            return '0'
                
                driver_dict = {'driver_name': [],
                                'driver_number': [],
                                'driver_color': [],
                                'lap': [],
                                'race': [],
                                'session': [],
                                'year': [],
                                'ft': [],
                                'rt': []}
                all_data = []
                cond = False
                
                for i in range(len(all_text)):
                    data = all_text[i].split(' ')
                    for d in drivers:
                        if d[:-2] in all_text[i]:
                            dr = d
                            col_ind = drivers.index(dr)
                            dn = data[1]
                            #drivers.remove(d)
                            #
                            if len(driver_dict['driver_name']) > 0:
                                all_data.append(driver_dict)
                                driver_dict = {'driver_name': [],
                                                'driver_number': [],
                                                'driver_color': [],
                                                'lap': [],
                                                'race': [],
                                                'session': [],
                                                'year': [],
                                                'ft': [],
                                                'rt': []}
                            break
                    a, b = tyre_to_num(data)

                    if a == 0:
                        ni = 1
                        nj = 2
                    elif a == 2:
                        ni = 0
                        nj = 0
                    elif a == 1 and b == 0:
                        ni = 0
                        nj = 1
                    elif a == 1 and b == 1:
                        ni = 1
                        nj = 1
                    if 'Front' in data:
                        ft = get_tyre(data[5-ni])
                    if 'Rear' in data:
                        rt = get_tyre(data[8-nj])

                    if 'Slick-MediumRear' in data:
                        ft = get_tyre(data[5].replace('Rear', ''))
                        rt = get_tyre(data[6].replace('Tyre', ''))
                    if data[0].isnumeric() and len(data)>=6:
                        
                        at = all_text[i].replace('  ', ' ')
                        at = at.replace('Race', '')
                        at = at.replace('MotoGP', '')
                        at = at.replace('Moto2', '')
                        at = at.replace('Moto3', '')    
                        at = at.replace('MotoGP', '')
                        at = at.replace('Free', '')
                        at = at.replace('d', '')
                        at = at.replace('i2', '')
                        at = at.replace('i1', '')
                        p_in = False
                        if 'P' in all_text[i][:20] or '*' in all_text[i][:20]:
                            p_in = True
                        at = at.replace('P', '')
                        at = at.replace('*', '')
                        at = at.replace('  ', ' ')
                        #if 'P' not in at:
                        data_ = at.split(' ')
                        driver_dict['driver_name'].append(dr)
                        driver_dict['driver_number'].append(dn)
                        driver_dict['driver_color'].append('#111111')
                        driver_dict['lap'].append(data_[0])
                        driver_dict['ft'].append(ft)
                        driver_dict['rt'].append(rt)
                        driver_dict['year'] = y
                        driver_dict['session'] = s 
                        driver_dict['race'] = race_id
                        if len(driver_dict['driver_name'])>0:
                            temp_df = pd.DataFrame(driver_dict)
                    if len(driver_dict['driver_name']) > 0:
                        t_df = pd.read_csv(f'/home/boris/Documents/matplotlib_exercize/tyre_type/tyre_type_{y}.csv')
                        t_df = pd.concat([t_df, temp_df], ignore_index=True)
                        t_df = t_df.drop_duplicates(keep='last')
                        t_df.to_csv(f'/home/boris/Documents/matplotlib_exercize/tyre_type/tyre_type_{y}.csv', index=False)

                #except:
                #    continue
            ft = 'n/a'
            rt = 'n/a'