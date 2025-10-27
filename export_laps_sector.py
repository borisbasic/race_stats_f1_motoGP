
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
from statistics import mean
sns.set_theme()
plt.style.use('ggplot')

def to_miliseconds(time):
    if len(time)>6:
        minutes = int(time.split(':')[0])*60000
        seconds = int(time.split(':')[1].split('.')[0])*1000
        miliseconds = int(time.split('.')[1])
        return minutes+seconds+miliseconds
    else:
        seconds = int(time.split('.')[0])*1000
        miliseconds = int(time.split('.')[1])
        return seconds+miliseconds
    
def to_real_time(t):
    new_time = str(t)
    minutes = int(new_time.split('.')[0])//60
    seconds = int(new_time.split('.')[0])%60
    miliseconds = int(new_time.split('.')[1])
    if seconds < 10:
        seconds = f'0{seconds}'
    if miliseconds < 10:
        miliseconds = f'00{miliseconds}'
    elif miliseconds < 100:
        miliseconds = f'0{miliseconds}'
    return f'{minutes}:{seconds}.{miliseconds}'

def clear_speed(s):
    s1 = ''
    for i in range(len(s)):
        if s[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
            s1 = s1 + s[i]
    
class_moto = os.listdir('/home/boris/Documents/matplotlib_exercize/moto_pdfs')
images_moto = '/home/boris/Documents/motogp_api/images'

for cm in class_moto:
    important_things_csv = '/home/boris/Documents/matplotlib_exercize/done/laps_sector.csv'
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
                
                fold = f'{images_moto}/{cm}/{y}/{r}/{s}'

                if not os.path.exists(f'{fold}/race'):
                    os.mkdir(f'{fold}/race')
                if not os.path.exists(f'{fold}/sector_1'):
                    os.mkdir(f'{fold}/sector_1')
                if not os.path.exists(f'{fold}/sector_2'):   
                    os.mkdir(f'{fold}/sector_2')
                if not os.path.exists(f'{fold}/sector_3'):   
                    os.mkdir(f'{fold}/sector_3')
                if not os.path.exists(f'{fold}/sector_4'):   
                    os.mkdir(f'{fold}/sector_4')

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
                    driver_team = row['team'].strip()
                    try:
                        color = bikes[(bikes['team']==driver_team) & (bikes['year']==year_)]['hex_color'].values[0]
                    except:
                        color = '#808080'
                    drivers_colors.append(color)

                for d in drivers_:
                    try:
                        help = pd.read_csv(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/{d}_analysis.csv')
                        
                    except:
                        continue
                    a_df = help
                    dri.append(d)
                    ind = drivers_.index(d)
                    dri_n.append(drivers_numbers[ind])
                    dr_c.append(drivers_colors[ind])
                    a_df['driver_color'] = drivers_colors[ind]

                    #------------------- Race
                    a_df['driver_number'] = drivers_numbers[ind]
                    avg_lap_time_reg = a_df['time'].mean()
                    str_avg = str(avg_lap_time_reg)
                    avg_lap_time_reg_min = int(str_avg.split('.')[0])//60
                    avg_lap_time_reg_sec = int(str_avg.split('.')[0])%60
                    avg_lap_time_reg_milisec = str_avg.split('.')[1][:3]

                    a_df['real_time'] = a_df['time'].apply(to_real_time)

                    a_df['time_milisec'] = a_df['time']*1000#.apply(to_miliseconds)
                    max_y = a_df['time_milisec'].max() + 2000
                    a_df['stacked_bar'] = max_y-a_df['time_milisec']
                    max_y_5 = max_y*1.0/5
                    ticks = [max_y_5*i for i in range(1, 6)]
                    avg_lap_time = a_df['time_milisec'][1:].mean()

                    labels = []

                    for t in ticks:
                        minutes = int(t / 60000)
                        seconds = int((t-minutes*60000)/1000)
                        labels.append(f'{minutes}:{seconds}')
                    fig, ax = plt.subplots(figsize =(12, 9), facecolor='#eaeaea')
                    ax.vlines(x=avg_lap_time, ymin=-1, ymax=len(a_df)+1, colors='black', 
                            label=f'Average lap time: {avg_lap_time_reg_min}:{avg_lap_time_reg_sec}.{avg_lap_time_reg_milisec}')
                    ax.yaxis.set_ticks(list(range(1, len(a_df)+1)), labels=[f'lap {i}' for i in range(1, len(a_df)+1)], fontname='Ubuntu', fontweight='bold',
                                fontsize=15,)
                    ax.xaxis.set_ticks(ticks=ticks, labels=labels, fontweight='bold', fontname='Ubuntu',
                                fontsize=15,)
                    
                    ax.barh( y=a_df['lap'], alpha=0.8,  edgecolor='black', width=a_df['time_milisec'], 
                            color=a_df.loc[0, 'driver_color'])
                    
                    ax.set_facecolor('#eaeaea')
                    #plt.yticks(y_ticks)
                    j = 0
                    for i in ax.patches:
                        plt.text(i.get_width()-int(i.get_width()*0.15), i.get_y()+0.1,
                                a_df.loc[j, 'real_time'],
                                #fontweight='bold',
                                fontsize=16,
                                fontname='Ubuntu',
                                color='black')
                        j = j + 1
                    ax.barh(y=a_df['lap'], alpha=0.4, edgecolor='black', width=a_df['stacked_bar'], 
                            left=a_df['time_milisec'], color=a_df.loc[0, 'driver_color'])
                    
                    plt.title(f"#{a_df.loc[0, 'driver_number']}  {a_df.loc[0, 'driver_name']}")
                    plt.ylabel('Laps')
                    plt.xlabel('Driver lap time')
                    plt.tight_layout()
                    plt.legend(loc='upper left', fontsize=15)
                    #plt.show()
                    plt.savefig(f'{fold}/race/{d}_lap_times.jpg')
                    plt.close()
                        
                    #------------------- Sector 1
                    a_df['sector_1'] = a_df['sector_1'].fillna(a_df['sector_1'].mean())
                    avg_lap_time_reg = a_df['sector_1'].mean()
                    str_avg = str(avg_lap_time_reg)
                    avg_lap_time_reg_min = int(str_avg.split('.')[0])//60
                    avg_lap_time_reg_sec = int(str_avg.split('.')[0])%60
                    avg_lap_time_reg_milisec = str_avg.split('.')[1][:3]

                    a_df['real_time_sector_1'] = a_df['sector_1'].apply(to_real_time)

                    a_df['sector_1_milisec'] = a_df['sector_1']*1000#.apply(to_miliseconds)
                    max_y = a_df['sector_1_milisec'].max() + 2000
                    a_df['stacked_bar_sector_1'] = max_y-a_df['sector_1_milisec']
                    max_y_5 = max_y*1.0/5
                    ticks = [max_y_5*i for i in range(1, 6)]

                    avg_lap_time = a_df['sector_1_milisec'][1:].mean()

                    labels = []

                    for t in ticks:
                        minutes = int(t / 60000)
                        seconds = int((t-minutes*60000)/1000)
                        labels.append(f'{minutes}:{seconds}')
                    fig, ax = plt.subplots(figsize =(12, 9), facecolor='#eaeaea')
                    ax.vlines(x=avg_lap_time, ymin=-1, ymax=len(a_df)+1, colors='black', 
                            label=f'Average sector 1 time: {avg_lap_time_reg_min}:{avg_lap_time_reg_sec}.{avg_lap_time_reg_milisec}')
                    ax.yaxis.set_ticks(list(range(1, len(a_df)+1)), labels=[f'lap {i}' for i in range(1, len(a_df)+1)], fontname='Ubuntu', fontweight='bold',
                                fontsize=15,)
                    ax.xaxis.set_ticks(ticks=ticks, labels=labels, fontweight='bold', fontname='Ubuntu',
                                fontsize=15,)
                    
                    ax.barh( y=a_df['lap'], alpha=0.8,  edgecolor='black', width=a_df['sector_1_milisec'], 
                            color=a_df.loc[0, 'driver_color'])
                    
                    ax.set_facecolor('#eaeaea')
                    #plt.yticks(y_ticks)
                    j = 0
                    for i in ax.patches:
                        plt.text(i.get_width()-int(i.get_width()*0.15), i.get_y()+0.1,
                                a_df.loc[j, 'real_time_sector_1'],
                                #fontweight='bold',
                                fontsize=16,
                                fontname='Ubuntu',
                                color='black')
                        j = j + 1
                    ax.barh(y=a_df['lap'], alpha=0.4, edgecolor='black', width=a_df['stacked_bar_sector_1'], 
                            left=a_df['sector_1_milisec'], color=a_df.loc[0, 'driver_color'])
                    
                    plt.title(f"#{a_df.loc[0, 'driver_number']}  {a_df.loc[0, 'driver_name']}")
                    plt.ylabel('Laps')
                    plt.xlabel('Driver sector 1 time')
                    plt.tight_layout()
                    plt.legend(loc='upper left', fontsize=15)
                    #plt.show()
                    plt.savefig(f'{fold}/sector_1/{d}_lap_times.jpg')
                    plt.close()

                    #------------------- Sector 2
                    a_df['sector_2'] = a_df['sector_2'].fillna(a_df['sector_2'].mean())
                    avg_lap_time_reg = a_df['sector_2'].mean()
                    str_avg = str(avg_lap_time_reg)
                    avg_lap_time_reg_min = int(str_avg.split('.')[0])//60
                    avg_lap_time_reg_sec = int(str_avg.split('.')[0])%60
                    avg_lap_time_reg_milisec = str_avg.split('.')[1][:3]

                    a_df['real_time_sector_2'] = a_df['sector_2'].apply(to_real_time)

                    a_df['sector_2_milisec'] = a_df['sector_2']*1000#.apply(to_miliseconds)
                    max_y = a_df['sector_2_milisec'].max() + 2000
                    a_df['stacked_bar_sector_2'] = max_y-a_df['sector_2_milisec']
                    max_y_5 = max_y*1.0/5
                    ticks = [max_y_5*i for i in range(1, 6)]

                    avg_lap_time = a_df['sector_2_milisec'][1:].mean()

                    labels = []

                    for t in ticks:
                        minutes = int(t / 60000)
                        seconds = int((t-minutes*60000)/1000)
                        labels.append(f'{minutes}:{seconds}')
                    fig, ax = plt.subplots(figsize =(12, 9), facecolor='#eaeaea')
                    ax.vlines(x=avg_lap_time, ymin=-1, ymax=len(a_df)+1, colors='black', 
                            label=f'Average sector 2 time: {avg_lap_time_reg_min}:{avg_lap_time_reg_sec}.{avg_lap_time_reg_milisec}')
                    ax.yaxis.set_ticks(list(range(1, len(a_df)+1)), labels=[f'lap {i}' for i in range(1, len(a_df)+1)], fontname='Ubuntu', fontweight='bold',
                                fontsize=15,)
                    ax.xaxis.set_ticks(ticks=ticks, labels=labels, fontweight='bold', fontname='Ubuntu',
                                fontsize=15,)
                    
                    ax.barh( y=a_df['lap'], alpha=0.8,  edgecolor='black', width=a_df['sector_2_milisec'], 
                            color=a_df.loc[0, 'driver_color'])
                    
                    ax.set_facecolor('#eaeaea')
                    #plt.yticks(y_ticks)
                    j = 0
                    for i in ax.patches:
                        plt.text(i.get_width()-int(i.get_width()*0.15), i.get_y()+0.1,
                                a_df.loc[j, 'real_time_sector_2'],
                                #fontweight='bold',
                                fontsize=16,
                                fontname='Ubuntu',
                                color='black')
                        j = j + 1
                    ax.barh(y=a_df['lap'], alpha=0.4, edgecolor='black', width=a_df['stacked_bar_sector_2'], 
                            left=a_df['sector_2_milisec'], color=a_df.loc[0, 'driver_color'])
                    
                    plt.title(f"#{a_df.loc[0, 'driver_number']}  {a_df.loc[0, 'driver_name']}")
                    plt.ylabel('Laps')
                    plt.xlabel('Driver sector 2 time')
                    plt.tight_layout()
                    plt.legend(loc='upper left', fontsize=15)
                    #plt.show()
                    plt.savefig(f'{fold}/sector_2/{d}_lap_times.jpg')
                    plt.close()
                    

                    #------------------- Sector 3
                    a_df['sector_3'] = a_df['sector_3'].fillna(a_df['sector_3'].mean())
                    avg_lap_time_reg = a_df['sector_3'].mean()
                    str_avg = str(avg_lap_time_reg)
                    avg_lap_time_reg_min = int(str_avg.split('.')[0])//60
                    avg_lap_time_reg_sec = int(str_avg.split('.')[0])%60
                    avg_lap_time_reg_milisec = str_avg.split('.')[1][:3]

                    a_df['real_time_sector_3'] = a_df['sector_3'].apply(to_real_time)

                    a_df['sector_3_milisec'] = a_df['sector_3']*1000#.apply(to_miliseconds)
                    max_y = a_df['sector_3_milisec'].max() + 2000
                    a_df['stacked_bar_sector_3'] = max_y-a_df['sector_3_milisec']
                    max_y_5 = max_y*1.0/5
                    ticks = [max_y_5*i for i in range(1, 6)]

                    avg_lap_time = a_df['sector_3_milisec'][1:].mean()

                    labels = []

                    for t in ticks:
                        minutes = int(t / 60000)
                        seconds = int((t-minutes*60000)/1000)
                        labels.append(f'{minutes}:{seconds}')
                    fig, ax = plt.subplots(figsize =(12, 9), facecolor='#eaeaea')
                    ax.vlines(x=avg_lap_time, ymin=-1, ymax=len(a_df)+1, colors='black', 
                            label=f'Average sector 3 time: {avg_lap_time_reg_min}:{avg_lap_time_reg_sec}.{avg_lap_time_reg_milisec}')
                    ax.yaxis.set_ticks(list(range(1, len(a_df)+1)), labels=[f'lap {i}' for i in range(1, len(a_df)+1)], fontname='Ubuntu', fontweight='bold',
                                fontsize=15,)
                    ax.xaxis.set_ticks(ticks=ticks, labels=labels, fontweight='bold', fontname='Ubuntu',
                                fontsize=15,)
                    
                    ax.barh( y=a_df['lap'], alpha=0.8,  edgecolor='black', width=a_df['sector_3_milisec'], 
                            color=a_df.loc[0, 'driver_color'])
                    
                    ax.set_facecolor('#eaeaea')
                    #plt.yticks(y_ticks)
                    j = 0
                    for i in ax.patches:
                        plt.text(i.get_width()-int(i.get_width()*0.15), i.get_y()+0.1,
                                a_df.loc[j, 'real_time_sector_3'],
                                #fontweight='bold',
                                fontsize=16,
                                fontname='Ubuntu',
                                color='black')
                        j = j + 1
                    ax.barh(y=a_df['lap'], alpha=0.4, edgecolor='black', width=a_df['stacked_bar_sector_3'], 
                            left=a_df['sector_3_milisec'], color=a_df.loc[0, 'driver_color'])
                    
                    plt.title(f"#{a_df.loc[0, 'driver_number']}  {a_df.loc[0, 'driver_name']}")
                    plt.ylabel('Laps')
                    plt.xlabel('Driver sector 3 time')
                    plt.tight_layout()
                    plt.legend(loc='upper left', fontsize=15)
                    #plt.show()
                    plt.savefig(f'{fold}/sector_3/{d}_lap_times.jpg')
                    plt.close()


                    #------------------- Sector 4
                    a_df['sector_4'] = a_df['sector_4'].fillna(a_df['sector_4'].mean())
                    avg_lap_time_reg = a_df['sector_4'].mean()
                    str_avg = str(avg_lap_time_reg)
                    avg_lap_time_reg_min = int(str_avg.split('.')[0])//60
                    avg_lap_time_reg_sec = int(str_avg.split('.')[0])%60
                    avg_lap_time_reg_milisec = str_avg.split('.')[1][:3]

                    a_df['real_time_sector_4'] = a_df['sector_4'].apply(to_real_time)

                    a_df['sector_4_milisec'] = a_df['sector_4']*1000#.apply(to_miliseconds)
                    max_y = a_df['sector_4_milisec'].max() + 2000
                    a_df['stacked_bar_sector_4'] = max_y-a_df['sector_4_milisec']
                    max_y_5 = max_y*1.0/5
                    ticks = [max_y_5*i for i in range(1, 6)]

                    avg_lap_time = a_df['sector_4_milisec'][1:].mean()

                    labels = []

                    for t in ticks:
                        minutes = int(t / 60000)
                        seconds = int((t-minutes*60000)/1000)
                        labels.append(f'{minutes}:{seconds}')
                    fig, ax = plt.subplots(figsize =(12, 9), facecolor='#eaeaea')
                    ax.vlines(x=avg_lap_time, ymin=-1, ymax=len(a_df)+1, colors='black', 
                            label=f'Average sector 4 time: {avg_lap_time_reg_min}:{avg_lap_time_reg_sec}.{avg_lap_time_reg_milisec}')
                    ax.yaxis.set_ticks(list(range(1, len(a_df)+1)), labels=[f'lap {i}' for i in range(1, len(a_df)+1)], fontname='Ubuntu', fontweight='bold',
                                fontsize=15,)
                    ax.xaxis.set_ticks(ticks=ticks, labels=labels, fontweight='bold', fontname='Ubuntu',
                                fontsize=15,)
                    
                    ax.barh( y=a_df['lap'], alpha=0.8,  edgecolor='black', width=a_df['sector_4_milisec'], 
                            color=a_df.loc[0, 'driver_color'])
                    
                    ax.set_facecolor('#eaeaea')
                    #plt.yticks(y_ticks)
                    j = 0
                    for i in ax.patches:
                        plt.text(i.get_width()-int(i.get_width()*0.15), i.get_y()+0.1,
                                a_df.loc[j, 'real_time_sector_4'],
                                #fontweight='bold',
                                fontsize=16,
                                fontname='Ubuntu',
                                color='black')
                        j = j + 1
                    ax.barh(y=a_df['lap'], alpha=0.4, edgecolor='black', width=a_df['stacked_bar_sector_4'], 
                            left=a_df['sector_4_milisec'], color=a_df.loc[0, 'driver_color'])
                    
                    plt.title(f"#{a_df.loc[0, 'driver_number']}  {a_df.loc[0, 'driver_name']}")
                    plt.ylabel('Laps')
                    plt.xlabel('Driver sector 4 time')
                    plt.tight_layout()
                    plt.legend(loc='upper left', fontsize=15)
                    #plt.show()
                    plt.savefig(f'{fold}/sector_4/{d}_lap_times.jpg')
                    plt.close()
            important_done.append('yes')
            new_dict = {'race': important_races, 
                        'is_done': important_done, 
                        'year': important_years, 
                        'class': important_classes}
            new_df = pd.DataFrame(new_dict)
            new_df.to_csv('/home/boris/Documents/matplotlib_exercize/done/laps_sector.csv', index=False)