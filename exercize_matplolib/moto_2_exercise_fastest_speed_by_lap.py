import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('ggplot')

drivers = ['Fermin ALDEGUER', 'Joe ROBERTS', 'Manuel GONZALEZ', 'Sergio GARCIA', 
           'Albert ARENAS', 'Ai OGURA', 'Tony ARBOLINO', 'Jeremy ALCOBA', 'Celestino VIETTI', 
           'Somkiat CHANTRA', 'Filip SALAC', 'Izan GUEVARA', 'Zonta VD GOORBE', 'Deniz ÖNCÜ',
           'Matteo FERRARI', 'Mario AJI', 'Xavi CARDELUS', 'Jorge NAVARRO', 
           'Darryn BINDER', 'Xavier ARTIGAS', 'Jaume MASIA', 'Jake DIXON', 'Alonso LOPEZ',
           'Marcos RAMIREZ', 'Alex ESCRIG', 'Diogo MOREIRA', 'Barry BALTUS',
           'Dennis FOGGIA', 'Senna AGIUS', 'Bo BENDSNEYDER', 'Ayumu SASAKI', 'Aron CANET', 'Daniel MUÑOZ']
drivers_colors = ['#ffcf49', '#011663','#6475a6', '#fa2701', 
                  '#6475a6', '#fa2701', '#291515', '#011c53', '#e84003',
                  '#635f34', '#291515', '#017da3', '#cccbce', '#e84003',
                  '#6475a6', '#635f34', '#99999c', '#048d71',
                  '#18243b', '#8db9b5', '#7f0809', '#017da3', '#ffcf49',
                  '#011663', '#8db9b5', '#082a51', '#cccbce',
                  '#082a51', '#18243b', '#7f0809', '#011c53', '#99999c', '#7f0809']
drivers_number = ['54', '16', '18', '3', 
                  '75', '79', '14', '52', '13',
                  '35', '12', '28', '84', '53', 
                  '23', '34', '20', '9',
                  '15', '43', '5', '96', '21', 
                  '24', '11', '10', '7',
                  '71', '81', '64', '22', '44', '17']
drivers_colors_matching = ['']
def crop_and_extract_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all = ''
        for page in pdf.pages:
            first_page = page
            page_width = first_page.width
            page_height = first_page.height

            # Crop the left half of the page
            crop_box = (0, 0, page_width / 2 + 15, page_height-100)
            cropped_page = first_page.within_bbox(crop_box)

            crop_box_ = (page_width / 2 + 15, 0, page_width, page_height-100)
            cropped_page_ = first_page.within_bbox(crop_box_) 
            # Extract text from the cropped region
            text = cropped_page.extract_text()
            text_ = cropped_page_.extract_text()
            all = all + text + text_
    return all

pdf_path = "/home/boris/Documents/matplotlib_exercize/LE_MANS_2024_MOTO_2/Analysis.pdf"
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
            dn = drivers_number[col_ind]
            #add_lap_time = True
            drivers.remove(d)
            del drivers_colors[col_ind]
            del drivers_number[col_ind]
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
        at = at.replace('Moto2', '')
        at = at.replace('d', '')
        at = at.replace(' P', '')
        data_ = at.split(' ')
        driver_dict['driver_name'].append(dr)
        driver_dict['driver_number'].append(dn)
        driver_dict['driver_color'].append(driver_color)
        driver_dict['lap'].append(data_[0])
        driver_dict['time'].append(data_[1].replace("'", ':'))
        driver_dict['sector_1'].append(data_[2])
        driver_dict['sector_2'].append(data_[3])
        driver_dict['sector_3'].append(data_[4])
        driver_dict['sector_4'].append(data_[5])
        driver_dict['speed'].append(data_[6])
    if i == len(all_text) - 1:
        all_data.append(driver_dict)

def to_miliseconds(time):
    minutes = int(time.split(':')[0])*60000
    seconds = int(time.split(':')[1].split('.')[0])*1000
    miliseconds = int(time.split('.')[1])
    return minutes+seconds+miliseconds

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

plt.title('Fastest lap speed by driver')
plt.ylabel('Laps')
plt.xlabel('Driver speed')
plt.tight_layout()
plt.savefig('/home/boris/Documents/matplotlib_exercize/LE_MANS_2024_MOTO_2/Le_MANS_Fastest_Speed_By_lap.jpg')

