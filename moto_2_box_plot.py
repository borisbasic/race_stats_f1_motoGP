import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
from statistics import mean
sns.set_theme()
plt.style.use('ggplot')
num_of_laps = 25
num_of_drivers = 30
race = 'DEUTCHLAND'
season = '2024'

drivers = ['Fermin ALDEGUER', 'Joe ROBERTS', 'Manuel GONZALEZ', 'Sergio GARCIA', 
           'Albert ARENAS', 'Ai OGURA', 'Tony ARBOLINO', 'Jeremy ALCOBA', 'Celestino VIETTI', 
           'Somkiat CHANTRA', 'Filip SALAC', 'Izan GUEVARA', 'Zonta VD GOORBE', 'Deniz ÖNCÜ',
           'Matteo FERRARI', 'Mario AJI', 'Xavi CARDELUS', 'Jorge NAVARRO', 
           'Darryn BINDER', 'Xavier ARTIGAS', 'Jaume MASIA', 'Jake DIXON', 'Alonso LOPEZ',
           'Marcos RAMIREZ', 'Alex ESCRIG', 'Diogo MOREIRA', 'Barry BALTUS',
           'Dennis FOGGIA', 'Senna AGIUS', 'Bo BENDSNEYDER', 'Ayumu SASAKI', 'Aron CANET', 'Daniel MUÑOZ',
           'Mattia PASINI', 'Marcel SCHROTTE', 'Roberto GARCIA', 'Zonta VD GOORBERGH', 'Marcel SCHROTTER']
drivers_colors = ['#ffcf49', '#011663','#6475a6', '#fa2701', 
                  '#6475a6', '#fa2701', '#291515', '#011c53', '#e84003',
                  '#635f34', '#291515', '#017da3', '#cccbce', '#e84003',
                  '#6475a6', '#635f34', '#99999c', '#048d71',
                  '#18243b', '#8db9b5', '#7f0809', '#017da3', '#ffcf49',
                  '#011663', '#8db9b5', '#082a51', '#cccbce',
                  '#082a51', '#18243b', '#7f0809', '#011c53', '#99999c', '#7f0809',
                  '#991111', '#e84003', '#ffcf49', '#cccbce', '#e84003']

pdf_patg_final_results = f'/home/boris/Documents/matplotlib_exercize/{race}_{season}_MOTO_2/FinalResults.pdf'

with pdfplumber.open(pdf_patg_final_results) as pdf:
    page = pdf.pages[0]
    page_width = page.width
    page_height = page.height
    crop_box_1 = (110, 164, page_width-370, page_height - 200)
    text = page.within_bbox(crop_box_1).extract_text()
all_text = text.split('\n')
dri = []
dr_n = []
dr_c = []
for at in all_text:
    if at not in dri:
        dri.append(at)
for d in dri:
    ind = drivers.index(d)
    dr_c.append(drivers_colors[ind])
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

pdf_path = f"/home/boris/Documents/matplotlib_exercize/{race}_{season}_MOTO_2/Analysis.pdf"
text = crop_and_extract_text(pdf_path)
all_text = text.split('\n')
driver_dict = {'driver_name': [],
               'time': [],}
all_data = []
def to_miliseconds(time):
    if len(time)>6:
        minutes = int(time.split(':')[0])*60000
        seconds = int(time.split(':')[1].split('.')[0])*1000
        miliseconds = int(time.split('.')[1])
        return (minutes+seconds+miliseconds)/1000
    else:
        seconds = int(time.split('.')[0])*1000
        miliseconds = int(time.split('.')[1])
        return (seconds+miliseconds)/1000
    
for i in range(len(all_text)):
    data = all_text[i].split(' ')
    for d in drivers:
        if d in all_text[i]:
            dr = d
            #
            if len(driver_dict['driver_name']) > 0:
                all_data.append(driver_dict)
                driver_dict = {'driver_name': [],
                                'time': [],}
            break
    if data[0].isnumeric() and len(data)>=7:
        at = all_text[i].replace('*', '')
        at = at.replace('  ', ' ')
        at = at.replace('Race', '')
        at = at.replace('Moto2', '')
        at = at.replace('d', '')
        if 'P' not in at:
            data_ = at.split(' ')
            driver_dict['driver_name'].append(dr)
            driver_dict['time'].append(to_miliseconds(data_[1].replace("'", ':')))
    if i == len(all_text) - 1:
        all_data.append(driver_dict)



new_dict = {}
for ad in all_data:
    if len(ad['time']) < num_of_laps:
        for i in range(num_of_laps-len(ad['time'])):
            ad['time'].append(mean(ad['time']))
    new_dict[ad['driver_name'][0]] = ad['time']
for key, item in new_dict.items():
    print(f'{key} :{len(item)}')
a_df = pd.DataFrame(new_dict)

avg_time = a_df.mean()[0]
ticks = [int(avg_time)-1, int(avg_time), int(avg_time)+1, int(avg_time)+2, int(avg_time)+3]
xticks = [i for i in range(1, num_of_drivers+1)]

fig, ax = plt.subplots(figsize=(15, 9))

plt.ylim(int(avg_time)-0.2, int(avg_time)+3)

bplot = ax.boxplot(a_df,
                   patch_artist=True,)  # will be used to label x-ticks
# fill with colors
for patch, color in zip(bplot['boxes'], dr_c):
    patch.set_facecolor(color)

plt.xticks(ticks=xticks, labels=[f'{dri[x-1].split(" ")[1]}' for x in xticks], rotation='vertical', fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)
plt.yticks(ticks=ticks, labels=[f'{l} s' for l in ticks], fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)

plt.xlabel('Drivers', fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)
plt.ylabel('Times', fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)
plt.tight_layout()
plt.savefig(f'/home/boris/Documents/matplotlib_exercize/{race}_2024_MOTO_2/{race}_RACE_PACE.jpg')


fig, ax = plt.subplots(figsize=(15, 9))

plt.ylim(int(avg_time)-0.2, int(avg_time)+3)

vplot = ax.violinplot(a_df, showmeans=True, showmedians=True, showextrema=False, widths=0.7)

# fill with colors
i = 0
for patch in vplot['bodies']:
    patch.set_facecolor(dr_c[i])
    patch.set_alpha(0.6)
    patch.set_edgecolor('black')
    i = i + 1
#vplot['cmedians'].set_colors(drivers_colors)
plt.xticks(ticks=xticks, labels=[f'{dri[x-1].split(" ")[1]}' for x in xticks], rotation='vertical', fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)
plt.yticks(ticks=ticks, labels=[f'{l} s' for l in ticks], fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)

plt.xlabel('Drivers', fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)
plt.ylabel('Times', fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)
plt.tight_layout()
plt.savefig(f'/home/boris/Documents/matplotlib_exercize/{race}_2024_MOTO_2/{race}_RACE_PACE_Violin.jpg')