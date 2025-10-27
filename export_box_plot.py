
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
from statistics import mean
sns.set_theme()
plt.style.use('ggplot')
pd.options.mode.chained_assignment = None

def sort_by_values_len(dict):
    dict_len= {key: len(value) for key, value in dict.items()}
    import operator
    sorted_key_list = sorted(dict_len.items(), key=operator.itemgetter(1), reverse=True)
    sorted_dict = [{item[0]: dict[item [0]]} for item in sorted_key_list]
    return sorted_dict
class_moto = os.listdir('/home/boris/Documents/matplotlib_exercize/moto_pdfs')
images_moto = '/home/boris/Documents/motogp_api/images'
for cm in class_moto:
    important_things_csv = '/home/boris/Documents/matplotlib_exercize/done/box_violin.csv'
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
                    #try:
                    driver_team = row['team'].strip()
                    #except:
                    #    driver_team = 'MB Conveyors - Speed Up Racing'
                    try:
                        color = bikes[(bikes['team']==driver_team) & (bikes['year']==year_)]['hex_color'].values[0]
                    except:
                        color = '#808080'
                    drivers_colors.append(color)

                a_df_r = pd.DataFrame()
                a_df_s1 = pd.DataFrame()
                a_df_s2 = pd.DataFrame()
                a_df_s3 = pd.DataFrame()
                a_df_s4 = pd.DataFrame()

                for d in drivers_:
                    try:
                        help = pd.read_csv(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/{d}_analysis.csv')
                        a_df_r[d] = help['time']
                        a_df_r[d].fillna(a_df_r[d].mean(), inplace=True)
                        a_df_s1[d] = help['sector_1']
                        a_df_s1[d].fillna(a_df_s1[d].mean(), inplace=True)
                        a_df_s2[d] = help['sector_2']
                        a_df_s2[d].fillna(a_df_s2[d].mean(), inplace=True)
                        a_df_s3[d] = help['sector_3']
                        a_df_s3[d].fillna(a_df_s3[d].mean(), inplace=True)
                        a_df_s4[d] = help['sector_4']
                        a_df_s4[d].fillna(a_df_s4[d].mean(), inplace=True)
                        dri.append(d)
                        ind = drivers_.index(d)
                        dri_n.append(drivers_numbers[ind])
                        dr_c.append(drivers_colors[ind])
                    except:
                        continue
                num_of_drivers = len(dri)

                a = [a_df_r, a_df_s1, a_df_s2, a_df_s3, a_df_s4]
                a_names = ['race', 'sector 1', 'sector 2', 'sector 3', 'sector 4']
                j = 0
                for a_df in a:
                    a_df_ = a_df[a_df>0]
                    Q1 = a_df_.quantile(0.25)
                    Q3 = a_df_.quantile(0.75)
                    IQR = Q3 - Q1

                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR

                    df_filtered = a_df[(a_df >= lower_bound) & (a_df <= upper_bound)]

                    avg_time = df_filtered[df_filtered > 0].median().median()
                    df_filtered = df_filtered[df_filtered > 0]
                    lowest = df_filtered.min().min()
                    highest = df_filtered.max().max()
                    minus = avg_time - (avg_time+lowest)/2
                    plus = (avg_time+highest)/2 - avg_time
                    if plus>20:
                        plus = plus -20
                    if plus > 15:
                        plus = plus -15
                    if plus > 10:
                        plus = plus - 10
                    
                    fig, ax = plt.subplots(figsize=(15, 9))
                    if a_names[j] == 'race':
                        ticks = [round((avg_time)-minus,2), round((avg_time),2), round((avg_time)+plus,2)]# round((avg_time),2)+2,]# (avg_time)+3]
                        plt.ylim((avg_time)-minus-2, (avg_time)+plus+0.5)
                    else:
                        ticks = [round((avg_time)-minus,2), round((avg_time),2), round((avg_time)+plus,2)]# round((avg_time),2)+2,]# (avg_time)+3]
                        plt.ylim((avg_time)-minus-0.5, (avg_time)+plus+0.5)
                    xticks = [i for i in range(1, num_of_drivers+1)]

                    bplot = ax.boxplot(a_df,
                                    patch_artist=True,)  
                    
                    for patch, color in zip(bplot['boxes'], dr_c):
                        patch.set_facecolor(color)

                    plt.xticks(ticks=xticks, labels=[f'{dri[x-1].split(" ")[0][0]}. {dri[x-1].split(" ")[1]}' for x in xticks], rotation='vertical', fontweight='bold', fontname='Ubuntu',
                                            fontsize=15,)
                    plt.yticks(ticks=ticks, labels=[f'{l} s' for l in ticks], fontweight='bold', fontname='Ubuntu',
                                            fontsize=15,)

                    plt.xlabel('Drivers', fontweight='bold', fontname='Ubuntu',
                                            fontsize=15,)
                    plt.ylabel('Times', fontweight='bold', fontname='Ubuntu',
                                            fontsize=15,)
                    plt.tight_layout()
                    plt.savefig(f'{images_moto}/{cm}/{y}/{r}/{s}/box_plot_{a_names[j]}.jpg')


                    fig, ax = plt.subplots(figsize=(15, 9))

                    if a_names[j] == 'race':
                        ticks = [round((avg_time)-minus,2), round((avg_time),2), round((avg_time)+plus,2)]# round((avg_time),2)+2,]# (avg_time)+3]
                        plt.ylim((avg_time)-minus-2, (avg_time)+plus+0.5)
                    else:
                        ticks = [round((avg_time)-minus,2), round((avg_time),2), round((avg_time)+plus,2)]# round((avg_time),2)+2,]# (avg_time)+3]
                        plt.ylim((avg_time)-minus-0.5, (avg_time)+plus+0.5)
                    vplot = ax.violinplot(a_df, showmeans=True, showmedians=True, showextrema=False, widths=0.7)

                    i = 0
                    for patch in vplot['bodies']:
                        patch.set_facecolor(dr_c[i])
                        patch.set_alpha(0.6)
                        patch.set_edgecolor('black')
                        i = i + 1
                    plt.xticks(ticks=xticks, labels=[f'{dri[x-1].split(" ")[0][0]}. {dri[x-1].split(" ")[1]}' for x in xticks], rotation='vertical', fontweight='bold', fontname='Ubuntu',
                                            fontsize=15,)
                    plt.yticks(ticks=ticks, labels=[f'{l} s' for l in ticks], fontweight='bold', fontname='Ubuntu',
                                            fontsize=15,)

                    plt.xlabel('Drivers', fontweight='bold', fontname='Ubuntu',
                                            fontsize=15,)
                    plt.ylabel('Times', fontweight='bold', fontname='Ubuntu',
                                            fontsize=15,)
                    plt.tight_layout()
                    plt.savefig(f'{images_moto}/{cm}/{y}/{r}/{s}/violin_plot_{a_names[j]}.jpg')
                    j = j + 1

            important_done.append('yes')
            new_dict = {'race': important_races, 
                        'is_done': important_done, 
                        'year': important_years, 
                        'class': important_classes}
            new_df = pd.DataFrame(new_dict)
            new_df.to_csv('/home/boris/Documents/matplotlib_exercize/done/box_violin.csv', index=False)