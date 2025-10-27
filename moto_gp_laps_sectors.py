import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import matplotlib.patches as mpathes
sns.set_theme()
#plt.style.use('ggplot')

race = 'SILVERSTONE'
season = '2024'
if not os.path.isdir(f'{race}_{season}'):
    os.mkdir(f'{race}_{season}')
if not os.path.isdir(f'{race}_{season}/{race}_{season}_Analysis'):
    os.mkdir(f'{race}_{season}/{race}_{season}_Analysis')


if not os.path.isdir(f'{race}_{season}/{race}_{season}_Sector_1'):
    os.mkdir(f'{race}_{season}/{race}_{season}_Sector_1')

if not os.path.isdir(f'{race}_{season}/{race}_{season}_Sector_2'):
    os.mkdir(f'{race}_{season}/{race}_{season}_Sector_2')

if not os.path.isdir(f'{race}_{season}/{race}_{season}_Sector_3'):
    os.mkdir(f'{race}_{season}/{race}_{season}_Sector_3')

if not os.path.isdir(f'{race}_{season}/{race}_{season}_Sector_4'):
    os.mkdir(f'{race}_{season}/{race}_{season}_Sector_4')

drivers = [ 'Marc MARQUEZ', 'Marco BEZZECCHI', 'Alex MARQUEZ', 'Enea BASTIANINI', 'Brad BINDER', 
           'Fabio DI GIANNANTONI', 'Miguel OLIVEIRA', 'Pedro ACOSTA', 'Maverick VIÑALES', 'Raul FERNANDEZ',
           'Joan MIR', 'Alex RINS', 'Takaaki NAKAGAMI', 'Fabio QUARTARARO', 'Stefan BRADL', 'Luca MARINI',
           'Augusto FERNANDEZ', 'Jack MILLER', 'Franco MORBIDELLI', 'Lorenzo SAVADORI', 'Jorge MARTIN', 'Johann ZARCO',
           'Aleix ESPARGARO', 'Daniel PEDROSA',  'Pol ESPARGARO', 'Francesco BAGNAIA',]
drivers_colors = [ '#9aadd2', '#e1fa50', '#9aadd2', '#cc0001', '#a44721',
          '#e1fb4f', '#0254b8', '#990525', '#5bb33a', '#0254b8',
          '#fea011', '#072e7e', '#cecece', '#072e7e', '#fea011', '#fea011',
          '#990525', '#a44721', '#8432c5', '#5cb139', '#8432c5', '#cecece',
          '#5bb33a', '#a44721', '#990525', '#cc0001',]

def crop_and_extract_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all = ''
        for page in pdf.pages:
            first_page = page
            page_width = first_page.width
            page_height = first_page.height

            crop_box = (0, 0, page_width / 2 + 15, page_height-100)
            cropped_page = first_page.within_bbox(crop_box)

            crop_box_ = (page_width / 2 + 15, 0, page_width, page_height-100)
            cropped_page_ = first_page.within_bbox(crop_box_) 
            text = cropped_page.extract_text()
            text_ = cropped_page_.extract_text()
            all = all + text + text_
    return all

pdf_path = f"/home/boris/Documents/matplotlib_exercize/{race}_{season}/Analysis.pdf"
text = crop_and_extract_text(pdf_path)
all_text = text.split('\n')
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

for i in range(len(all_text)):
    data = all_text[i].split(' ')
    for d in drivers:
        if d in all_text[i]:
            dr = d
            col_ind = drivers.index(dr)
            driver_color = drivers_colors[col_ind]
            dn = data[1]
            #add_lap_time = True
            drivers.remove(d)
            del drivers_colors[col_ind]
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
    if data[0].isnumeric() and len(data)>=7:
        at = all_text[i].replace('*', '')
        at = at.replace('  ', ' ')
        at = at.replace('Race', '')
        at = at.replace('MotoGP', '')
        at = at.replace('d', '')
        if 'P' not in at:
            data_ = at.split(' ')
            driver_dict['driver_name'].append(dr)
            driver_dict['driver_number'].append(dn)
            driver_dict['driver_color'].append(driver_color)
            driver_dict['lap'].append(data_[0])
            driver_dict['time'].append(data_[1].replace("'", ':'))
            driver_dict['sector_1'].append(data_[2].replace("'", ':'))
            driver_dict['sector_2'].append(data_[3].replace("'", ':'))
            driver_dict['sector_3'].append(data_[4].replace("'", ':'))
            driver_dict['sector_4'].append(data_[5].replace("'", ':'))
            driver_dict['speed'].append(data_[6])
    if i == len(all_text) - 1:
        all_data.append(driver_dict)


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

for i in range(len(all_data)):    
    analysis_df = pd.DataFrame(all_data[i])
    if not analysis_df.empty:
        if len(analysis_df)>1:
            avg_lap_time_reg = pd.to_datetime(analysis_df['time'][1:], format="%M:%S.%f", errors='coerce').mean()
        else:
            avg_lap_time_reg = pd.to_datetime(analysis_df['time'], format="%M:%S.%f", errors='coerce').mean()
        avg_lap_time_reg_min = str(avg_lap_time_reg).split(' ')[1].split(':')[1]
        avg_lap_time_reg_sec = str(avg_lap_time_reg).split(' ')[1].split(':')[2].split('.')[0]
        avg_lap_time_reg_milisec = (str(avg_lap_time_reg).split(' ')[1].split(':')[2].split('.')[1][:3])
        analysis_df['time_milisec'] = analysis_df['time'].apply(to_miliseconds)
        analysis_df['speed'] = analysis_df['speed'].astype(float)
        max_y = analysis_df['time_milisec'].max() + 2000
        analysis_df['stacked_bar'] = max_y-analysis_df['time_milisec']
        max_y_5 = max_y*1.0/5
        ticks = [max_y_5*i for i in range(1, 6)]

        avg_lap_time = analysis_df['time_milisec'][1:].mean()

        labels = []
        for t in ticks:
            minutes = int(t / 60000)
            seconds = int((t-minutes*60000)/1000)
            labels.append(f'{minutes}:{seconds}')
        fig, ax = plt.subplots(figsize =(12, 9), facecolor='#eaeaea')
        ax.vlines(x=avg_lap_time, ymin=-1, ymax=len(analysis_df), colors='black', 
                label=f'Average lap time: {avg_lap_time_reg_min}:{avg_lap_time_reg_sec}.{avg_lap_time_reg_milisec}')
        ax.yaxis.set_ticks(list(range(0, len(analysis_df))), labels=[f'lap {i}' for i in range(1, len(analysis_df)+1)], fontname='Ubuntu', fontweight='bold',
                    fontsize=15,)
        ax.xaxis.set_ticks(ticks=ticks, labels=labels, fontweight='bold', fontname='Ubuntu',
                    fontsize=15,)
        
        ax.barh( y=analysis_df['lap'], alpha=0.8,  edgecolor='black', width=analysis_df['time_milisec'], 
                color=analysis_df.loc[0, 'driver_color'])
        
        ax.set_facecolor('#eaeaea')
        #plt.yticks(y_ticks)
        j = 0
        for i in ax.patches:
            plt.text(i.get_width()-int(i.get_width()*0.1), i.get_y()+0.1,
                    analysis_df.loc[j, 'time'],
                    #fontweight='bold',
                    fontsize=16,
                    fontname='Ubuntu',
                    color='black')
            j = j + 1
        ax.barh(y=analysis_df['lap'], alpha=0.4, edgecolor='black', width=analysis_df['stacked_bar'], 
                left=analysis_df['time_milisec'], color=analysis_df.loc[0, 'driver_color'])
        plt.title(f"#{analysis_df.loc[0, 'driver_number']}  {analysis_df.loc[0, 'driver_name']}")
        plt.ylabel('Laps')
        plt.xlabel('Driver lap time')
        plt.tight_layout()
        plt.legend(loc='upper left', fontsize=15)
        plt.savefig(f'/home/boris/Documents/matplotlib_exercize/{race}_{season}/{race}_{season}_Analysis/{analysis_df.loc[0, "driver_name"]}_analysis.jpg')
        plt.close()

for i in range(len(all_data)):    
    analysis_df = pd.DataFrame(all_data[i])
    
    if not analysis_df.empty:
        if len(analysis_df)>1:
            avg_lap_time_reg = pd.to_datetime(analysis_df['sector_1'][1:], format="%S.%f", errors='coerce').mean()
        else:
            avg_lap_time_reg = pd.to_datetime(analysis_df['sector_1'], format="%S.%f", errors='coerce').mean()
        avg_lap_time_reg_sec = str(avg_lap_time_reg).split(' ')[1].split(':')[2].split('.')[0]
        avg_lap_time_reg_milisec = (str(avg_lap_time_reg).split(' ')[1].split(':')[2].split('.')[1][:3])
        analysis_df['time_milisec'] = analysis_df['sector_1'].apply(to_miliseconds)
        analysis_df['speed'] = analysis_df['speed'].astype(float)
        max_y = analysis_df['time_milisec'].max() + 2000
        analysis_df['stacked_bar'] = max_y-analysis_df['time_milisec']
        max_y_5 = max_y*1.0/5
        ticks = [max_y_5*i for i in range(1, 6)]

        avg_lap_time = analysis_df['time_milisec'][1:].mean()

        labels = []
        for t in ticks:
            minutes = int(t / 60000)
            seconds = int((t-minutes*60000)/1000)
            labels.append(f'{minutes}:{seconds}')

        fig, ax = plt.subplots(figsize =(12, 9), facecolor='#eaeaea')
        ax.vlines(x=avg_lap_time, ymin=-1, ymax=len(analysis_df), colors='black', 
                label=f'Average sector 1 time: {avg_lap_time_reg_sec}.{avg_lap_time_reg_milisec}')
        ax.yaxis.set_ticks(list(range(0, len(analysis_df))), labels=[f'lap {i}' for i in range(1, len(analysis_df)+1)], fontname='Ubuntu', fontweight='bold',
                    fontsize=15,)
        ax.xaxis.set_ticks(ticks=ticks, labels=labels, fontweight='bold', fontname='Ubuntu',
                    fontsize=15,)
        ax.barh( y=analysis_df['lap'], alpha=0.8,  edgecolor='black', width=analysis_df['time_milisec'], color=analysis_df.loc[0, 'driver_color'])
        ax.set_facecolor('#eaeaea')
        #plt.yticks(y_ticks)
        j = 0
        for i in ax.patches:
            plt.text(i.get_width()-int(i.get_width()*0.1), i.get_y()+0.1,
                    analysis_df.loc[j, 'sector_1'],
                    #fontweight='bold',
                    fontsize=16,
                    fontname='Ubuntu',
                    color='black')
            j = j + 1
        ax.barh(y=analysis_df['lap'], alpha=0.4, edgecolor='black', width=analysis_df['stacked_bar'], 
            left=analysis_df['time_milisec'], color=analysis_df.loc[0, 'driver_color'])

        plt.title(f"#{analysis_df.loc[0, 'driver_number']}  {analysis_df.loc[0, 'driver_name']}")
        plt.ylabel('Laps')
        plt.xlabel('Driver sector 1 time')
        plt.tight_layout()
        plt.legend(loc='upper left', fontsize=15)
        plt.savefig(f'/home/boris/Documents/matplotlib_exercize/{race}_{season}/{race}_{season}_Sector_1/{analysis_df.loc[0, "driver_name"]}_sector_1.jpg')
        plt.close()


for i in range(len(all_data)):    
    analysis_df = pd.DataFrame(all_data[i])
    if not analysis_df.empty:
        avg_lap_time_reg = pd.to_datetime(analysis_df['sector_2'], format="%S.%f", errors='coerce').mean()
        avg_lap_time_reg_sec = str(avg_lap_time_reg).split(' ')[1].split(':')[2].split('.')[0]
        avg_lap_time_reg_milisec = (str(avg_lap_time_reg).split(' ')[1].split(':')[2].split('.')[1][:3])
        analysis_df['time_milisec'] = analysis_df['sector_2'].apply(to_miliseconds)
        analysis_df['speed'] = analysis_df['speed'].astype(float)
        max_y = analysis_df['time_milisec'].max() + 2000
        analysis_df['stacked_bar'] = max_y-analysis_df['time_milisec']
        max_y_5 = max_y*1.0/5
        ticks = [max_y_5*i for i in range(1, 6)]

        avg_lap_time = analysis_df['time_milisec'][1:].mean()

        labels = []
        for t in ticks:
            minutes = int(t / 60000)
            seconds = int((t-minutes*60000)/1000)
            labels.append(f'{minutes}:{seconds}')

        fig, ax = plt.subplots(figsize =(12, 9), facecolor='#eaeaea')
        ax.vlines(x=avg_lap_time, ymin=-1, ymax=len(analysis_df), colors='black', 
                label=f'Average sector 2 time: {avg_lap_time_reg_sec}.{avg_lap_time_reg_milisec}')
        ax.yaxis.set_ticks(list(range(0, len(analysis_df))), labels=[f'lap {i}' for i in range(1, len(analysis_df)+1)], fontname='Ubuntu', fontweight='bold',
                    fontsize=15,)
        ax.xaxis.set_ticks(ticks=ticks, labels=labels, fontweight='bold', fontname='Ubuntu',
                    fontsize=15,)
        ax.barh( y=analysis_df['lap'], edgecolor='black', alpha=0.8,  width=analysis_df['time_milisec'], color=analysis_df.loc[0, 'driver_color'])
        ax.set_facecolor('#eaeaea')
        #plt.yticks(y_ticks)
        j = 0
        for i in ax.patches:
            plt.text(i.get_width()-int(i.get_width()*0.1), i.get_y()+0.1,
                    analysis_df.loc[j, 'sector_2'],
                    #fontweight='bold',
                    fontsize=16,
                    fontname='Ubuntu',
                    color='black')
            j = j + 1
        ax.barh(y=analysis_df['lap'], alpha=0.4, edgecolor='black', width=analysis_df['stacked_bar'], 
            left=analysis_df['time_milisec'], color=analysis_df.loc[0, 'driver_color'])
        plt.title(f"#{analysis_df.loc[0, 'driver_number']}  {analysis_df.loc[0, 'driver_name']}")
        plt.ylabel('Laps')
        plt.xlabel('Driver sector 2 time')
        plt.tight_layout()
        plt.legend(loc='upper left', fontsize=15)
        plt.savefig(f'/home/boris/Documents/matplotlib_exercize/{race}_{season}/{race}_{season}_Sector_2/{analysis_df.loc[0, "driver_name"]}_sector_2.jpg')
        plt.close()


for i in range(len(all_data)):    
    analysis_df = pd.DataFrame(all_data[i])
    if not analysis_df.empty:
        avg_lap_time_reg = pd.to_datetime(analysis_df['sector_3'], format="%S.%f", errors='coerce').mean()
        avg_lap_time_reg_min = str(avg_lap_time_reg).split(' ')[1].split(':')[1]
        avg_lap_time_reg_sec = str(avg_lap_time_reg).split(' ')[1].split(':')[2].split('.')[0]
        avg_lap_time_reg_milisec = (str(avg_lap_time_reg).split(' ')[1].split(':')[2].split('.')[1][:3])
        analysis_df['time_milisec'] = analysis_df['sector_3'].apply(to_miliseconds)
        analysis_df['speed'] = analysis_df['speed'].astype(float)
        max_y = analysis_df['time_milisec'].max() + 2000
        analysis_df['stacked_bar'] = max_y-analysis_df['time_milisec']
        max_y_5 = max_y*1.0/5
        ticks = [max_y_5*i for i in range(1, 6)]

        avg_lap_time = analysis_df['time_milisec'][1:].mean()

        labels = []
        for t in ticks:
            minutes = int(t / 60000)
            seconds = int((t-minutes*60000)/1000)
            labels.append(f'{minutes}:{seconds}')

        fig, ax = plt.subplots(figsize =(12, 9), facecolor='#eaeaea')
        ax.vlines(x=avg_lap_time, ymin=-1, ymax=len(analysis_df), colors='black', 
                label=f'Average sector 3 time: {avg_lap_time_reg_sec}.{avg_lap_time_reg_milisec}')
        ax.yaxis.set_ticks(list(range(0, len(analysis_df))), labels=[f'lap {i}' for i in range(1, len(analysis_df)+1)], fontname='Ubuntu', fontweight='bold',
                    fontsize=15,)
        ax.xaxis.set_ticks(ticks=ticks, labels=labels, fontweight='bold', fontname='Ubuntu',
                    fontsize=15,)
        ax.barh( y=analysis_df['lap'], edgecolor='black', alpha=0.8,  width=analysis_df['time_milisec'], color=analysis_df.loc[0, 'driver_color'])
        ax.set_facecolor('#eaeaea')
        #plt.yticks(y_ticks)
        j = 0
        for i in ax.patches:
            plt.text(i.get_width()-int(i.get_width()*0.1), i.get_y()+0.1,
                    analysis_df.loc[j, 'sector_3'],
                    #fontweight='bold',
                    fontsize=16,
                    fontname='Ubuntu',
                    color='black')
            j = j + 1
        ax.barh(y=analysis_df['lap'], alpha=0.4, edgecolor='black', width=analysis_df['stacked_bar'], 
            left=analysis_df['time_milisec'], color=analysis_df.loc[0, 'driver_color'])
        plt.title(f"#{analysis_df.loc[0, 'driver_number']}  {analysis_df.loc[0, 'driver_name']}")
        plt.ylabel('Laps')
        plt.xlabel('Driver sector 3 time')
        plt.tight_layout()
        plt.legend(loc='upper left', fontsize=15)
        plt.savefig(f'/home/boris/Documents/matplotlib_exercize/{race}_{season}/{race}_{season}_Sector_3/{analysis_df.loc[0, "driver_name"]}_sector_3.jpg')
        plt.close()

for i in range(len(all_data)):    
    analysis_df = pd.DataFrame(all_data[i])
    if not analysis_df.empty:
        avg_lap_time_reg = pd.to_datetime(analysis_df['sector_4'], format="%S.%f", errors='coerce').mean()
        avg_lap_time_reg_sec = str(avg_lap_time_reg).split(' ')[1].split(':')[2].split('.')[0]
        avg_lap_time_reg_milisec = (str(avg_lap_time_reg).split(' ')[1].split(':')[2].split('.')[1][:3])
        analysis_df['time_milisec'] = analysis_df['sector_4'].apply(to_miliseconds)
        analysis_df['speed'] = analysis_df['speed'].astype(float)
        max_y = analysis_df['time_milisec'].max() + 2000
        analysis_df['stacked_bar'] = max_y-analysis_df['time_milisec']
        max_y_5 = max_y*1.0/5
        ticks = [max_y_5*i for i in range(1, 6)]

        avg_lap_time = analysis_df['time_milisec'][1:].mean()

        labels = []
        for t in ticks:
            minutes = int(t / 60000)
            seconds = int((t-minutes*60000)/1000)
            labels.append(f'{minutes}:{seconds}')

        fig, ax = plt.subplots(figsize =(12, 9), facecolor='#eaeaea')
        ax.vlines(x=avg_lap_time, ymin=-1, ymax=len(analysis_df), colors='black', 
                label=f'Average sector 4 time: {avg_lap_time_reg_sec}.{avg_lap_time_reg_milisec}')
        ax.yaxis.set_ticks(list(range(0, len(analysis_df))), labels=[f'lap {i}' for i in range(1, len(analysis_df)+1)], fontname='Ubuntu', fontweight='bold',
                    fontsize=15,)
        ax.xaxis.set_ticks(ticks=ticks, labels=labels, fontweight='bold', fontname='Ubuntu',
                    fontsize=15,)
        ax.barh( y=analysis_df['lap'], edgecolor='black', alpha=0.8,  width=analysis_df['time_milisec'], color=analysis_df.loc[0, 'driver_color'])
        ax.set_facecolor('#eaeaea')
        #plt.yticks(y_ticks)
        j = 0
        for i in ax.patches:
            plt.text(i.get_width()-int(i.get_width()*0.1), i.get_y()+0.1,
                    analysis_df.loc[j, 'sector_4'],
                    #fontweight='bold',
                    fontsize=16,
                    fontname='Ubuntu',
                    color='black')
            j = j + 1
        ax.barh(y=analysis_df['lap'], alpha=0.4, edgecolor='black', width=analysis_df['stacked_bar'], 
            left=analysis_df['time_milisec'], color=analysis_df.loc[0, 'driver_color'])
        plt.title(f"#{analysis_df.loc[0, 'driver_number']}  {analysis_df.loc[0, 'driver_name']}")
        plt.ylabel('Laps')
        plt.xlabel('Driver sector 4 time')
        plt.tight_layout()
        plt.legend(loc='upper left', fontsize=15)
        plt.savefig(f'/home/boris/Documents/matplotlib_exercize/{race}_{season}/{race}_{season}_Sector_4/{analysis_df.loc[0, "driver_name"]}_sector_4.jpg')
        plt.close()



#################################
# Fastest lap by laps
data = pd.DataFrame(all_data[0])

for i in range(1, len(all_data)):    
    fastest_lap = pd.DataFrame(all_data[i])
    data = pd.concat([data, fastest_lap], axis=0, ignore_index=True)
    
fastest_laps = pd.DataFrame()
for i in range(1, 26):
    data_by_lap = data[data['lap']==str(i)]
    data_by_lap['time_milisec'] = data_by_lap['time'].apply(to_miliseconds)
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
ax.yaxis.set_ticks(list(range(0, len(fastest_laps))), labels=[f'lap {i}' for i in range(1, len(fastest_laps)+1)], 
                   fontname='Ubuntu', fontweight='bold',
                fontsize=15,)
ax.xaxis.set_ticks(ticks=ticks, labels=labels, fontweight='bold', fontname='Ubuntu',
                fontsize=15,)
ax.set_facecolor('#eaeaea')

j = 0
for i in ax.patches:
    plt.text(i.get_width()-int(i.get_width()*0.45), i.get_y()+0.1,
            f'#{str(fastest_laps.loc[j, "driver_number"])} - {str(fastest_laps.loc[j, "driver_name"])} - {str(fastest_laps.loc[j, "time"])}',
            fontsize=16,
            fontname='Ubuntu',
            color='black')
    j = j + 1
ax.barh(y=fastest_laps['lap'], alpha=0.4, edgecolor='black', width=fastest_laps['stacked_bar'], 
                left=fastest_laps['time_milisec'], color=fastest_laps['driver_color'])
l = mpathes.Patch(color=the_fastest_color,
                   label=f'Fastest lap by {the_fastest.loc[0, "driver_name"]} - {the_fastest.loc[0, "time"]}')
plt.title('Fastest lap speed by driver')
plt.ylabel('Laps')
plt.xlabel('Driver speed')
plt.tight_layout()
ax.legend(handles=[l], loc=(0,-0.08), fontsize=13)
plt.savefig(f'/home/boris/Documents/matplotlib_exercize/{race}_{season}/{race}_Fastest_Lap_By_lap.jpg')



#####################################
# Fastest speed by lap


data = pd.DataFrame(all_data[0])
for i in range(1, len(all_data)):    
    fastest_lap = pd.DataFrame(all_data[i])
    data = pd.concat([data, fastest_lap], axis=0, ignore_index=True)
    
fastest_laps = pd.DataFrame()
for i in range(1, 26):
    data_by_lap = data[data['lap']==str(i)]
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
ax.yaxis.set_ticks(list(range(0, len(fastest_laps))), labels=[f'lap {i}' for i in range(1, len(fastest_laps)+1)], 
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
plt.savefig(f'/home/boris/Documents/matplotlib_exercize/{race}_{season}/{race}_Fastest_Speed_By_lap.jpg')




