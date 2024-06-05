import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
plt.style.use('ggplot')

drivers = ['Collin VEIJER', 'David MUÑOZ', 'Ivan ORTOLA', 'Ryusei YAMANAKA', 'Joel KELSO',
           'Adrian FERNANDEZ', 'Daniel HOLGADO', 'Nicola CARRARO', 'Stefano NEPA', 'Angel PIQUERAS',
           'David ALONSO', 'Jacob ROULSTONE', 'Filippo FARIOLI', 'Matteo BERTELLE', 'David ALMANSA',
           'Vicente PEREZ', 'Taiyo FURUSATO', 'Riccardo ROSSI', 'Scott OGDEN', 'Luca LUNETTA',
           'Noah DETTWILER', 'Xabi ZURUTUZA', 'Joshua WHATLEY', 'Tatchakorn BUASRI', 'Tatsuki SUZUKI',
           'Joel ESTEBAN', 'Hamad AL-SAHOUTI', 'Jose Antonio RUEDA']
drivers_colors = ['#081830', '#0581bc', '#e85903', '#e85903', '#0581bc',
                  '#46b2c6', '#6d0406', '#d60057', '#d60057', '#46b2c6',
                  '#01799d', '#6d0406', '#9d9ea0', '#c7b705', '#c7b705', 
                  '#c82305', '#6d6f71', '#00a601', '#e6e8ec', '#9d9ea0',
                  '#00a601', '#c82305', '#e6e8ec', '#6d6f71', '#081830',
                  '#01799d', '#c7b705', '#c82305']
drivers_number = ['95', '64', '48', '6', '66',
                  '31', '96', '10', '82', '36',
                  '80', '12', '7', '18', '22', 
                  '21', '72', '54', '19','58',
                  '55', '85', '70', '5', '24', 
                  '78', '71', '99']
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

pdf_path = "/home/boris/Documents/matplotlib_exercize/LE_MANS_2024_MOTO_3/Analysis.pdf"
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
        at = at.replace('Moto3', '')
        at = at.replace('d', '')
        if not 'P' in at:
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
plt.savefig('/home/boris/Documents/matplotlib_exercize/LE_MANS_2024_MOTO_3/LE_MANS_Fastest_Lap_By_lap.jpg')
#plt.show()

