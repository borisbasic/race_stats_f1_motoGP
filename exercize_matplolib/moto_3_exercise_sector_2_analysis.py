import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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
        if 'P' not in at:
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
    seconds = int(time.split('.')[0])*1000
    miliseconds = int(time.split('.')[1])
    return seconds+miliseconds
for i in range(len(all_data)):    
    analysis_df = pd.DataFrame(all_data[i])
    if not analysis_df.empty:
        avg_lap_time_reg = pd.to_datetime(analysis_df['sector_2'], format="%S.%f").mean()
        avg_lap_time_reg_min = str(avg_lap_time_reg).split(' ')[1].split(':')[1]
        avg_lap_time_reg_sec = str(avg_lap_time_reg).split(' ')[1].split(':')[2].split('.')[0]
        avg_lap_time_reg_milisec = (str(avg_lap_time_reg).split(' ')[1].split(':')[2].split('.')[1][:3])
        analysis_df['time_milisec'] = analysis_df['sector_2'].apply(to_miliseconds)
        #analysis_df['sector_1'] = pd.to_datetime(analysis_df['sector_1'], format="%S.%f")
        #analysis_df['sector_2'] = pd.to_datetime(analysis_df['sector_2'], format="%S.%f")
        #analysis_df['sector_3'] = pd.to_datetime(analysis_df['sector_3'], format="%S.%f")
        #analysis_df['sector_4'] = pd.to_datetime(analysis_df['sector_4'], format="%S.%f")
        analysis_df['speed'] = analysis_df['speed'].astype(float)
        max_y = analysis_df['time_milisec'].max() + 1000
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

        plt.title(f"#{analysis_df.loc[0, 'driver_number']}  {analysis_df.loc[0, 'driver_name']}")
        plt.ylabel('Laps')
        plt.xlabel('Driver sector 2 time')
        plt.tight_layout()
        plt.legend(loc='upper left', fontsize=15)
        plt.savefig(f'/home/boris/Documents/matplotlib_exercize/LE_MANS_2024_MOTO_3/LE_MANS_2024_Sector_2/{analysis_df.loc[0, "driver_name"]}_sector_2.jpg')
        plt.close()