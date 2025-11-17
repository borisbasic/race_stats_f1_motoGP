
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import matplotlib.patches as mpathes
from statistics import mean
sns.set_theme()
plt.style.use('ggplot')

pd.options.mode.chained_assignment = None
def clear_speed(s):
    s1 = ''
    s = str(s)
    for i in range(len(s)):
        if s[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
            s1 = s1 + s[i]
    return float(s1)
    #return float(s)

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

def sort_by_values_len(dict):
    dict_len= {key: len(value) for key, value in dict.items()}
    import operator
    sorted_key_list = sorted(dict_len.items(), key=operator.itemgetter(1), reverse=True)
    sorted_dict = [{item[0]: dict[item [0]]} for item in sorted_key_list]
    return sorted_dict
class_moto = os.listdir('/home/boris/Documents/matplotlib_exercize/moto_pdfs')

images_moto = '/home/boris/Documents/motogp_api/images'

for cm in class_moto:
    important_things_csv = '/home/boris/Documents/matplotlib_exercize/done/speed.csv'
    important_things_csv = pd.read_csv(important_things_csv)
    important_races = important_things_csv['race'].tolist()
    important_years = important_things_csv['year'].tolist()
    important_classes = important_things_csv['class'].tolist()
    important_done = important_things_csv['is_done'].tolist()
    important_session = important_things_csv['session'].tolist()
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
           
            list_of_races = os.listdir(f'{images_moto}/{cm}/{y}')
            
            if r not in list_of_races:
                os.mkdir(f'{images_moto}/{cm}/{y}/{r}')
            seasion = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}')
            for s in seasion:
                dones = important_things_csv[(important_things_csv['race'] == r) & (important_things_csv['year'] == int(y)) & (important_things_csv['class'] == cm) & (important_things_csv['session'] == s)]['is_done'].tolist()
            
                if 'yes' in dones:
                    continue
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
                    driver_team = row['team'].strip()
                    try:
                        color = bikes[(bikes['team']==driver_team) & (bikes['year']==year_)]['hex_color'].values[0]
                    except:
                        color = "#693B116C"
                    drivers_colors.append(color)

                a_df_r = pd.DataFrame()
                num_of_lap = 0
                for d in drivers_:
                    try:
                        help = pd.read_csv(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/{d}_analysis.csv')
                        if num_of_lap <= len(help):
                            num_of_lap = len(help)
                        
                        dri.append(d)
                        ind = drivers_.index(d)
                        dri_n.append(drivers_numbers[ind])
                        dr_c.append(drivers_colors[ind])
                        help['driver_color'] = drivers_colors[ind]
                        help['real_time'] = help['time'].apply(to_real_time)
                        help['driver_number'] = drivers_numbers[ind]
                        help['speed'] = help['speed'].apply(clear_speed)
                        a_df_r = pd.concat([a_df_r, help])
                    except:
                        continue
                num_of_drivers = len(dri)
                    
                fastest_laps = pd.DataFrame()
                for i in range(1, num_of_lap+1):
                    data_by_lap = a_df_r[a_df_r['lap']==(i)]
                    data_by_lap['time_milisec'] = data_by_lap['time']*1000
                    fast = data_by_lap['time_milisec'].min()
                    fastest = data_by_lap[data_by_lap['time_milisec']==fast].head(1)
                    if fastest_laps.empty:
                        fastest_laps = fastest
                    else:
                        fastest_laps = pd.concat([fastest_laps, fastest], axis=0, ignore_index=True)
                the_fastest = fastest_laps[fastest_laps['time_milisec'] == fastest_laps['time_milisec'].min()].reset_index()
                the_fastest_color = the_fastest.loc[0, 'driver_color']
                max_y = fastest_laps['time_milisec'].max() + 2000
                fastest_laps['stacked_bar'] = max_y-fastest_laps['time_milisec']
                max_y_5 = max_y*1.0/5
                ticks = [max_y_5*i for i in range(1, 6)]
                labels = []
                for t in ticks:
                    minutes = int(t / 60000)
                    seconds = int((t-minutes*60000)/1000)
                    labels.append(f'{minutes}:{seconds}')
                fig, ax = plt.subplots(figsize =(12, 9), facecolor='#eaeaea')
                ax.barh(y=fastest_laps['lap'], alpha=0.8,  edgecolor='black', width=fastest_laps['time_milisec'], 
                        color=fastest_laps['driver_color'], )
                ax.yaxis.set_ticks(list(range(1, len(fastest_laps)+1)), labels=[f'lap {i}' for i in range(1, len(fastest_laps)+1)], 
                                fontname='Ubuntu', fontweight='bold',
                                fontsize=15,)
                ax.xaxis.set_ticks(ticks=ticks, labels=labels, fontweight='bold', fontname='Ubuntu',
                                fontsize=15,)
                ax.set_facecolor('#eaeaea')

                j = 0
                for i in ax.patches:
                    plt.text(i.get_width()-int(i.get_width()*0.45), i.get_y()+0.1,
                            f'#{str(fastest_laps.loc[j, "driver_number"])} - {str(fastest_laps.loc[j, "driver_name"])} - {str(fastest_laps.loc[j, "real_time"])}',
                            fontsize=16,
                            fontname='Ubuntu',
                            color='black')
                    j = j + 1
                ax.barh(y=fastest_laps['lap'], alpha=0.4, edgecolor='black', width=fastest_laps['stacked_bar'], 
                                left=fastest_laps['time_milisec'], color=fastest_laps['driver_color'])
                l = mpathes.Patch(color=the_fastest_color,
                                label=f'Fastest lap by {the_fastest.loc[0, "driver_name"]} - {the_fastest.loc[0, "real_time"]}')
                plt.title('Fastest lap speed by driver')
                plt.ylabel('Laps')
                plt.xlabel('Driver speed')
                plt.tight_layout()
                ax.legend(handles=[l], loc=(0,-0.08), fontsize=13)
                plt.savefig(f'{images_moto}/{cm}/{y}/{r}/{s}/Fastest_Lap_By_lap.jpg')


                plt.close()

                fastest_laps = pd.DataFrame()
                for i in range(1, 26):
                    data_by_lap = a_df_r[a_df_r['lap']==(i)]
                    data_by_lap['speed'] = data_by_lap['speed'].astype(float)
                    fast = data_by_lap['speed'].max()
                    fastest = data_by_lap[data_by_lap['speed']==fast].head(1)
                    if fastest_laps.empty:
                        fastest_laps = fastest
                    else:
                        fastest_laps = pd.concat([fastest_laps, fastest], axis=0, ignore_index=True)
                the_fastest = fastest_laps[fastest_laps['speed'] == fastest_laps['speed'].max()].reset_index()
                the_fastest_color = the_fastest.loc[0, 'driver_color']
                max_speed = fastest_laps['speed'].max()+5
                fastest_laps['stacked_bar'] = max_speed - fastest_laps['speed'] 
                fig, ax = plt.subplots(figsize =(12, 9), facecolor='#eaeaea')
                ax.barh(y=fastest_laps['lap'], alpha=0.8,  edgecolor='black', width=fastest_laps['speed'], 
                        color=fastest_laps['driver_color'])
                ax.yaxis.set_ticks(list(range(1, len(fastest_laps)+1)), labels=[f'lap {i}' for i in range(1, len(fastest_laps)+1)], 
                                fontname='Ubuntu', fontweight='bold',
                                fontsize=15,)
                ax.set_facecolor('#eaeaea')

                j = 0
                for i in ax.patches:
                    plt.text(i.get_width()-int(i.get_width()*0.45), i.get_y()+0.1,
                            f'#{str(fastest_laps.loc[j, "driver_number"])} - {str(fastest_laps.loc[j, "driver_name"])} - {str(fastest_laps.loc[j, "speed"])} km/h',
                            fontsize=16,
                            fontname='Ubuntu',
                            color='black')
                    j = j + 1
                ax.barh(y=fastest_laps['lap'], alpha=0.4, edgecolor='black', width=fastest_laps['stacked_bar'], 
                                left=fastest_laps['speed'], color=fastest_laps['driver_color'])
                l = mpathes.Patch(color=the_fastest_color,
                                label=f'Fastest driver by {the_fastest.loc[0, "driver_name"]} - {the_fastest.loc[0, "speed"]}')
                plt.title('Fastest lap speed by driver')
                plt.ylabel('Laps')
                plt.xlabel('Driver speed')
                plt.tight_layout()
                ax.legend(handles=[l], loc=(0,-0.08), fontsize=13)
                plt.savefig(f'{images_moto}/{cm}/{y}/{r}/{s}/Fastest_Speed_By_lap.jpg')

                important_done.append('yes')
                important_races.append(r)
                important_years.append(y)
                important_classes.append(cm)
                important_session.append(s)
                new_dict = {'race': important_races, 
                            'is_done': important_done, 
                            'year': important_years, 
                            'class': important_classes,
                            'session': important_session}
                new_df = pd.DataFrame(new_dict)
                new_df.to_csv('/home/boris/Documents/matplotlib_exercize/done/speed.csv', index=False)