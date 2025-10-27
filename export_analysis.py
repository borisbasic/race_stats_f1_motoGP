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
    important_things_csv = '/home/boris/Documents/matplotlib_exercize/done/analysis.csv'
    important_things_csv = pd.read_csv(important_things_csv)
    important_races = important_things_csv['race'].tolist()
    important_years = important_things_csv['year'].tolist()
    important_classes = important_things_csv['class'].tolist()
    important_sessions = important_things_csv['session'].tolist()
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
            
            list_of_races = os.listdir(f'{images_moto}/{cm}/{y}')
            
            if r not in list_of_races:
                os.mkdir(f'{images_moto}/{cm}/{y}/{r}')
            seasion = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}')
            for s in seasion:
                dones = important_things_csv[(important_things_csv['race'] == r) & (important_things_csv['year'] == int(y)) & (important_things_csv['class'] == cm) & (important_things_csv['session'] == s)]['is_done'].tolist()
            
                if 'yes' in dones:
                    continue

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
                drivers = drivers['driver_name'].to_list()

                def crop_and_extract_text(pdf_path):
                    with pdfplumber.open(pdf_path) as pdf:
                        all = ''
                        for page in pdf.pages:
                            first_page = page
                            page_width = first_page.width
                            page_height = first_page.height

                            crop_box = (0, 0, page_width / 2 + 10, page_height-120)
                            cropped_page = first_page.within_bbox(crop_box)

                            crop_box_ = (page_width / 2 + 10, 0, page_width , page_height-120)
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
                            'time': [],
                            'sector_1': [],
                            'sector_2': [],
                            'sector_3': [],
                            'sector_4': [],
                            'speed': []}
                all_data = []
                cond = False
                for i in range(len(all_text)):
                    data = all_text[i].split(' ')
                    for d in drivers:
                        if d[:-1] in all_text[i]:
                            dr = d
                            col_ind = drivers.index(dr)
                            dn = data[1]
                            drivers.remove(d)
                            #
                            if len(driver_dict['driver_name']) > 0:
                                all_data.append(driver_dict)
                                driver_dict = {'driver_name': [],
                                                'driver_number': [],
                                                'driver_color': [],
                                                'lap': [],
                                                'time': [],
                                                'sector_1': [],
                                                'sector_2': [],
                                                'sector_3': [],
                                                'sector_4': [],
                                                'speed': []}
                            break
                    if data[0].isnumeric() and len(data)>=6:
                        
                        at = all_text[i].replace('P', '')
                        at = at.replace('*', '')
                        at = at.replace('  ', ' ')
                        at = at.replace('Race', '')
                        at = at.replace('MotoGP', '')
                        at = at.replace('Moto2', '')
                        at = at.replace('Moto3', '')    
                        at = at.replace('MotoG™', '')
                        at = at.replace('Free', '')
                        at = at.replace('d', '')
                        at = at.replace('i2', '')
                        at = at.replace('i1', '')
                        
                        #if 'P' not in at:
                        data_ = at.split(' ')
                        driver_dict['driver_name'].append(dr)
                        driver_dict['driver_number'].append(dn)
                        driver_dict['driver_color'].append('#111111')
                        driver_dict['lap'].append(data_[0])
                        try:
                            driver_dict['time'].append(data_[1].replace("'", ':'))
                        except:
                            driver_dict['time'].append('0')
                        try:
                            driver_dict['sector_1'].append(data_[2].replace("'", ':'))
                        except:   
                            driver_dict['sector_1'].append('0')
                        try:
                            driver_dict['sector_2'].append(data_[3].replace("'", ':'))
                        except:
                            driver_dict['sector_2'].append('0')
                        try:
                            driver_dict['sector_3'].append(data_[4].replace("'", ':'))
                        except:
                            driver_dict['sector_3'].append('0')
                        try:
                            driver_dict['sector_4'].append(data_[5].replace("'", ':'))
                        except:
                            driver_dict['sector_4'].append('0')
                        try:
                            driver_dict['speed'].append(data_[6])
                        except:
                            driver_dict['speed'].append('0')
                        if len(driver_dict['driver_name'])>0:
                            temp_df = pd.DataFrame(driver_dict)
                            temp_df['time'] = temp_df['time'].apply(lambda x: to_miliseconds(x))
                            temp_df['time'] = temp_df['time'].astype(float)
                            temp_df['time'] = temp_df['time'].fillna(temp_df['time'].mean())
                            temp_df['sector_1'] = temp_df['sector_1'].apply(lambda x: to_miliseconds(x))
                            temp_df['sector_1'] = temp_df['sector_1'].astype(float)
                            temp_df['sector_1'] = temp_df['sector_1'].fillna(temp_df['sector_1'].mean())
                            temp_df['sector_2'] = temp_df['sector_2'].apply(lambda x: to_miliseconds(x))
                            temp_df['sector_2'] = temp_df['sector_2'].astype(float)
                            temp_df['sector_2'] = temp_df['sector_2'].fillna(temp_df['sector_2'].mean())
                            temp_df['sector_3'] = temp_df['sector_3'].apply(lambda x: to_miliseconds(x))
                            temp_df['sector_3'] = temp_df['sector_3'].astype(float)
                            temp_df['sector_3'] = temp_df['sector_3'].fillna(temp_df['sector_3'].mean())
                            temp_df['sector_4'] = temp_df['sector_4'].apply(lambda x: to_miliseconds(x))
                            temp_df['sector_4'] = temp_df['sector_4'].astype(float)
                            temp_df['sector_4'] = temp_df['sector_4'].fillna(temp_df['sector_4'].mean())
                            temp_df.to_csv(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/{dr}_analysis.csv', index=False)
                    else:
                        continue
                    if i == len(all_text) - 1:
                        all_data.append(driver_dict)
                important_races.append(r)
                important_years.append(y)
                important_classes.append(cm)
                important_sessions.append(s)
                important_done.append('yes')
                new_dict = {'race': important_races, 
                            'is_done': important_done, 
                            'year': important_years, 
                            'class': important_classes,
                            'session': important_sessions}
                new_df = pd.DataFrame(new_dict)
                new_df.to_csv('/home/boris/Documents/matplotlib_exercize/done/analysis.csv', index=False)


                #except:
                #    continue