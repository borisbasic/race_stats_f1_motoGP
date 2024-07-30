import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import bar_chart_race as bcr
sns.set_theme()
plt.style.use('ggplot')


race = 'BELGIA'
season = '2024'

if not os.path.isdir(f'{race}_{season}_F1/{race}_{season}_Analysis'):
    os.mkdir(f'{race}_{season}_F1/{race}_{season}_Analysis')

drivers = ['Max VERSTAPPEN', 'Sergio PEREZ', 'Charles LECLERC', 'Lando NORRIS', 'Carlos SAINZ',
            'Oscar PIASTRI', 'George RUSSELL', 'Fernando ALONSO', 'Lewis HAMILTON', 'Yuki TSUNODA', 'Lance STROLL', 
           'Oliver BEARMAN', 'Nico HULKENBERG', 'Daniel RICCIARDO', 'Esteban OCON', 'Kevin MAGNUSSEN', 
           'Alexander ALBON', 'ZHOU Guanyu', 'Pierre GASLY', 'Valtteri BOTTAS', 'Logan SARGEANT']
drivers_colors = ['#3671c6', '#3671c6', '#d92e37', '#c15206', '#d92e37',
                  '#c15206', '#27f4d2', '#037c78', '#27f4d2', '#6692ff', '#037c78',
                  '#d92e37', '#b6babd', '#6692ff', '#0093cc', '#b6babd',
                  '#64c4ff', '#76c97b', '#0093cc', '#76c97b', '#64c4ff']
drivers_numbers = [1, 11, 16, 4, 55,
                   81,  63, 14, 44, 22, 18,
                   12, 27, 3, 31, 20,
                   23, 24, 10, 77, 2]
pdf_patg_final_results = f'/home/boris/Documents/matplotlib_exercize/{race}_{season}_F1/Final_Results.pdf'

with pdfplumber.open(pdf_patg_final_results) as pdf:
    page = pdf.pages[0]
    page_width = page.width
    page_height = page.height
    crop_box_1 = (50, 164, page_width-450, page_height - 100)
    text = page.within_bbox(crop_box_1).extract_text()
all_text = text.split('\n')
dr = []
dr_n = []
dr_c = []
for at in all_text:
    if at not in dr:
        dr.append(at)
del dr[0]
for d in dr:
    ind = drivers.index(d)
    dr_n.append(drivers_numbers[ind])
    dr_c.append(drivers_colors[ind])
pdf_path = f'/home/boris/Documents/matplotlib_exercize/{race}_{season}_F1/Lap_Times.pdf'
text = ''
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        page_width = page.width
        page_height = page.height
        x = 125
        crop_box_1 = (0, 164, x, page_height-70)
        crop_box_2 = (x, 164, 2*x-5, page_height-70)
        crop_box_3 = (2*x-5, 164, 3*x-25, page_height-70)
        crop_box_4 = (3*x-25, 164, 4*x-35, page_height-70)
        crop_box_5 = (4*x-35, 164, page_width, page_height-70)
        cropped_page_1 = page.within_bbox(crop_box_1)
        cropped_page_2 = page.within_bbox(crop_box_2)
        cropped_page_3 = page.within_bbox(crop_box_3)
        cropped_page_4 = page.within_bbox(crop_box_4)
        cropped_page_5 = page.within_bbox(crop_box_5)
        text = text + cropped_page_1.extract_text() + '\n' + \
                cropped_page_2.extract_text() + '\n' + \
                cropped_page_3.extract_text() + '\n' + \
                cropped_page_4.extract_text() + '\n' + \
                cropped_page_5.extract_text() + '\n' 

all_data = text.split('\n')
for ad in all_data:
    if ad == '':
        all_data.remove(ad)

laps = []

for ad in all_data:
    if 'LAP' in ad and 'TIME' in ad:
        laps.append(ad.split(' ')[1])

laps_times = pd.DataFrame(index=laps, columns=dr_n)
laps_times.fillna('0', inplace=True)
num_of_lap = 0
for ad in all_data:
    if 'LAP' in ad and 'TIME' in ad:
        num_of_lap = (ad.split(' ')[1])
    if 'LAP' not in ad:
        row = ad.split(' ')
        if len(row) == 2:
            laps_times.loc[num_of_lap, int(row[0])] = str(row[1])
        elif len(row) == 3:
            if 'PIT' in row:
                laps_times.loc[num_of_lap, int(row[0])] = str(row[2])
            else:
                laps_times.loc[num_of_lap, int(row[0])] = str(row[2])
    elif 'LAP' in ad and 'TIME' not in ad:
        row = ad.split(' ')
        laps_times.loc[num_of_lap, int(row[0])] = str(row[3])


def to_miliseconds(time):
    if len(time)>6:
        minutes = int(time.split(':')[0])*60000
        seconds = int(time.split(':')[1].split('.')[0])*1000
        miliseconds = int(time.split('.')[1])
        return (minutes+seconds+miliseconds)*1.0/1000
    elif time == '0':
        return int(time)
    else:
        seconds = int(time.split('.')[0])*1000
        miliseconds = int(time.split('.')[1])
        return (seconds+miliseconds)*1.0/1000
    

for col in laps_times:
    laps_times[col] = laps_times[col].apply(to_miliseconds)



change_driver_name = []
for col in laps_times: 
    ind_of_dr = dr_n.index(int(col))
    change_driver_name.append(dr[ind_of_dr])

laps_times = laps_times.set_axis(change_driver_name, axis=1,)

#laps_times.to_csv(f'/home/boris/Documents/matplotlib_exercize/{race}_{season}_F1/lap_chart_1.csv')
#laps_times = laps_times.drop(columns=['Oliver BEARMAN'])
laps_times[laps_times==0] = np.nan
ticks = [105, 110, 115,]
xticks = [i for i in range(1, 21)]
drivers.remove('Oliver BEARMAN')
fig, ax = plt.subplots(figsize=(15, 9))

plt.ylim(105, 115)

bplot = ax.boxplot(laps_times,
                   patch_artist=True,)  # will be used to label x-ticks

# fill with colors
for patch, color, driver in zip(bplot['boxes'], dr_c, drivers):
    patch.set_facecolor(color)

plt.xticks(ticks=xticks, labels=[f'{dr[x-1].split(" ")[1]}' for x in xticks], rotation='vertical', fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)
plt.yticks(ticks=ticks, labels=[f'{l} s' for l in ticks], fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)

plt.xlabel('Drivers', fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)
plt.ylabel('Times', fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)
plt.tight_layout()
plt.savefig(f'/home/boris/Documents/matplotlib_exercize/{race}_2024_F1/RACE_PACE.jpg')


fig, ax = plt.subplots(figsize=(15, 9))

plt.ylim(105, 115)

vplot = ax.violinplot(laps_times, showmeans=True, showmedians=True, showextrema=False, widths=0.7)

# fill with colors
i = 0
for patch in vplot['bodies']:
    patch.set_facecolor(dr_c[i])
    patch.set_alpha(0.6)
    patch.set_edgecolor('black')
    i = i + 1
vplot['cmedians'].set_colors(dr_c)
plt.xticks(ticks=xticks, labels=[f'{dr[x-1].split(" ")[1]}' for x in xticks], rotation='vertical', fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)
plt.yticks(ticks=ticks, labels=[f'{l} s' for l in ticks], fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)

plt.xlabel('Drivers', fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)
plt.ylabel('Times', fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)
plt.tight_layout()
plt.savefig(f'/home/boris/Documents/matplotlib_exercize/{race}_2024_F1/RACE_PACE_Violin.jpg')
