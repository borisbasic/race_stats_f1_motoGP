
import pandas as pd
import matplotlib.pyplot as plt
import os
import pdfplumber
def sort_by_values_len(dict):
    dict_len= {key: len(value) for key, value in dict.items()}
    import operator
    sorted_key_list = sorted(dict_len.items(), key=operator.itemgetter(1), reverse=True)
    sorted_dict = [{item[0]: dict[item [0]]} for item in sorted_key_list]
    return sorted_dict
class_moto = os.listdir('/home/boris/Documents/matplotlib_exercize/moto_pdfs')
images_moto = '/home/boris/Documents/motogp_api/images'

for cm in class_moto:
    important_things_csv = '/home/boris/Documents/matplotlib_exercize/done/race_plot_line.csv'
    important_things_csv = pd.read_csv(important_things_csv)
    important_races = important_things_csv['race'].tolist()
    important_years = important_things_csv['year'].tolist()
    important_classes = important_things_csv['class'].tolist()
    important_done = important_things_csv['is_done'].tolist()
    important_sessions = important_things_csv['session'].tolist()
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
                bikes = '/home/boris/Documents/matplotlib_exercize/all_drivers_with_colors.csv'
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
                
                a_df_r = pd.DataFrame()
                time_dict = {}
                num_of_lap = 0
                pdf_path = f"/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/LapChart.pdf"
                try:
                    with pdfplumber.open(pdf_path) as pdf:
                        page = pdf.pages[0]
                        page_width = page.width
                        page_height = page.height
                        crop_box = (0, 130, page_width, page_height-100)
                        cropped_page = page.within_bbox(crop_box)
                        text = cropped_page.extract_text()
                except:
                    continue
                    
                all_text = text.split('\n')
                start_position = all_text[0].split(' ')[1:]
                starting_grid = all_text[1].split(' ')[1:]

                num_of_drivers = len(start_position)

                laps_order_dict = {'start_position': start_position,
                                'starting_grid': starting_grid}
                laps_order = []

                for i in range(2, len(all_text)):
                    line = all_text[i].split(' ')
                    if line[0].isalpha() and len(line)>2:
                        new_line = line[2:]
                        if len(new_line) != num_of_drivers:
                            add_spaces = num_of_drivers - len(new_line)
                            for i in range(add_spaces):
                                new_line.append('0')
                        laps_order_dict[f'lap {line[1]}'] = new_line
                        laps_order.append(new_line)
                    elif len(line)>1:
                        new_line = line[1:]
                        if len(new_line) != num_of_drivers:
                            add_spaces = num_of_drivers - len(new_line)
                            for i in range(add_spaces):
                                new_line.append('0')
                        laps_order_dict[f'lap {line[0]}'] = new_line
                        laps_order.append(new_line)


                num_of_laps = len(laps_order) 
                to_plot = {}
                for dn in laps_order_dict['starting_grid']:
                    to_plot[str(dn)] = []
                    for key, item in laps_order_dict.items():
                        for i in item:
                            if str(dn) == i:
                                if key != 'start_position':
                                    to_plot[str(dn)].append(num_of_drivers  - (item.index(i)))
                to_plot = sort_by_values_len(to_plot)
                tp_dict = {}
                for tp in to_plot:
                    tp_dict[list(tp.items())[0][0]] = list(tp.items())[0][1]

                to_plot = tp_dict
                i = num_of_drivers
                for key, item in to_plot.items():
                    if len(item) < num_of_laps+1:
                        iters = num_of_laps - len(item) + 1
                        for _ in range(iters):
                            item.append(i)
                    i = i - 1
                
                ticks = [i for i in range(0, num_of_laps+1)]
                labels = [f'{int(t)}' for t in ticks]
                labels[0] = 'Start'
                labels[-1] = f"{num_of_laps}"
                not_finish_driver = 0
                plt.figure(figsize=(15,9))
                plt.xticks(ticks=ticks, labels=labels, fontweight='bold', fontname='Ubuntu',
                                        fontsize=15,)
                plt.xlim([-1, num_of_laps+12])
                plt.yticks(list(range(1, len(start_position)+1)), labels=[f'{num_of_drivers+1-i}' for i in range(1, len(start_position)+1)], 
                                    fontname='Ubuntu', fontweight='bold',
                                    fontsize=15,)
                plt.ylim([0, len(start_position)+2])
                for dn in laps_order_dict['starting_grid']:
                    try:
                        driver_to_plot = str(dn)
                        ind_of_number = dri_n.index((driver_to_plot))
                        color_of_driver_to_plot = dr_c[ind_of_number]
                        drvier = dri[ind_of_number]
                    except:
                        continue
                    if len(to_plot[driver_to_plot])>0:
                        plt.plot(to_plot[driver_to_plot], color=color_of_driver_to_plot, label=drvier, lw=2)

                        plt.tight_layout()

                        plt.ylabel('Position', fontname='Ubuntu', fontweight='bold', fontsize=15)
                        plt.xlabel('Laps', fontname='Ubuntu', fontweight='bold', fontsize=15)
                        plt.text(num_of_laps+1.2, to_plot[driver_to_plot][-1], drvier, fontsize=16,
                                    fontname='Ubuntu',
                                    color=color_of_driver_to_plot)
                        plt.title(f'{r} {y} - {cm.upper()}', fontname='Ubuntu', fontweight='bold', fontsize=15)
                #mplcursors.cursor(hover=True)
                plt.savefig(f'{images_moto}/{cm}/{y}/{r}/{s}/line_plot_all.jpg')
                #plt.show()

                important_done.append('yes')
                important_sessions.append(s)
                important_races.append(r)
                important_years.append(y)
                important_classes.append(cm)
                new_dict = {'race': important_races, 
                            'is_done': important_done, 
                            'year': important_years, 
                            'class': important_classes,
                            'session': important_sessions}
                new_df = pd.DataFrame(new_dict)
                new_df.to_csv('/home/boris/Documents/matplotlib_exercize/done/race_plot_line.csv', index=False)