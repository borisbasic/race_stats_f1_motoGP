import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
sns.set_theme()
plt.style.use('ggplot')

class_moto = os.listdir('/home/boris/Documents/matplotlib_exercize/moto_pdfs')
def equal_time(row):
    time = row['sector_1'] + row['sector_2'] + row['sector_3'] + row['sector_4']
    if time - row['time'] < 0.001 and time - row['time'] > -0.001:
        return 'yes'
    else:
        return 'no'
images_moto = '/home/boris/Documents/motogp_api/images'

for cm in class_moto:
    important_things_csv = '/home/boris/Documents/matplotlib_exercize/done/fastest_lap.csv'
    important_things_csv = pd.read_csv(important_things_csv)
    important_races = important_things_csv['race'].tolist()
    important_years = important_things_csv['year'].tolist()
    important_classes = important_things_csv['class'].tolist()
    important_done = important_things_csv['is_done'].tolist()
    if cm not in ['motogp', 'moto2', 'moto3']:
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
                if s not in ['rac', 'spr']:
                    continue
                list_of_seasion = os.listdir(f'{images_moto}/{cm}/{y}/{r}')
                if s not in list_of_seasion:
                    os.mkdir(f'{images_moto}/{cm}/{y}/{r}/{s}')

                if not os.path.exists(f"/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/Analysis.pdf"):
                        continue
                drivers = f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/entry.csv'
                bikes = '/home/boris/Documents/matplotlib_exercize/all_drivers_with_colors.csv'
                try:
                    drivers = pd.read_csv(drivers)
                except:
                    continue
                bikes = pd.read_csv(bikes)
                drivers_ = []
                drivers_colors = []
                drivers_numbers = []
                dri = []
                dr_c = []
                dri_n = []
                year_ = int(y)
                for i, row in drivers.iterrows():
                    if row['rider_surname'] == 'RUEDA Jose':
                        rueda = row['rider_surname'].split(' ')[1] + ' ' + row['rider_name'] + ' ' + row['rider_surname'].split(' ')[0]
                        drivers_.append(rueda)
                    else:
                        drivers_.append(f'{row["rider_name"]} {row["rider_surname"]}')
                    drivers_numbers.append(f'{row["number"]}')
                    try:
                        driver_team = row['team'].strip()
                        color = bikes[(bikes['team']==driver_team) & (bikes['year']==year_)]['hex_color'].values[0]
                    except:
                        color = '#808080'
                    drivers_colors.append(color)
                fs_1 = 0
                fs_1_driver = ''
                fs_2 = 0
                fs_2_driver = ''
                fs_3 = 0
                fs_3_driver = ''
                fs_4 = 0
                fs_4_driver = ''
                for d in drivers_:
                    try:
                        help = pd.read_csv(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/{d}_analysis.csv')
                        
                        help['yes'] = help.apply(equal_time, axis=1)
                        help = help[help['yes'] == 'yes']
                    except:
                        continue
                    if fs_1 == 0:
                        fs_1 = help[help['sector_1'] > 0]['sector_1'].min()
                        fs_1_driver = d
                        fs_2 = help[help['sector_2'] > 0]['sector_2'].min()
                        fs_2_driver = d
                        fs_3 = help[help['sector_3'] > 0]['sector_3'].min()
                        fs_3_driver = d
                        fs_4 = help[help['sector_4'] > 0]['sector_4'].min()
                        fs_4_driver = d
                        continue
                    
                    fs_1_help = help[help['sector_1'] > 0]['sector_1'].min()
                    fs_2_help = help[help['sector_2'] > 0]['sector_2'].min()
                    fs_3_help = help[help['sector_3'] > 0]['sector_3'].min()
                    fs_4_help = help[help['sector_4'] > 0]['sector_4'].min()

                    if fs_1_help < fs_1:
                        fs_1 = fs_1_help
                        fs_1_driver = d
                    if fs_2_help < fs_2:
                        fs_2 = fs_2_help
                        fs_2_driver = d
                    if fs_3_help < fs_3:
                        fs_3 = fs_3_help
                        fs_3_driver = d     
                    if fs_4_help < fs_4:
                        fs_4 = fs_4_help
                        fs_4_driver = d
                lap_time = fs_1 + fs_2 + fs_3 + fs_4
                lap_time = round(lap_time, 3)
                fastets_lap_dict = {
                    'lap_time': lap_time,
                    'sector_1': fs_1,
                    'sector_1_driver': fs_1_driver,
                    'sector_2': fs_2,
                    'sector_2_driver': fs_2_driver,
                    'sector_3': fs_3,
                    'sector_3_driver': fs_3_driver,
                    'sector_4': fs_4,
                    'sector_4_driver': fs_4_driver
                }
                fastest_lap_df = pd.DataFrame([fastets_lap_dict])
                fastest_lap_df.to_csv(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/fastest_lap.csv', index=False)
            
            important_done.append('yes')
            new_dict = {'race': important_races, 
                        'is_done': important_done, 
                        'year': important_years, 
                        'class': important_classes}
            new_df = pd.DataFrame(new_dict)
            new_df.to_csv('/home/boris/Documents/matplotlib_exercize/done/fastest_lap.csv', index=False)