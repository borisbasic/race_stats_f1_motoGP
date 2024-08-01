import pdfplumber
import pandas as pd
import bar_chart_race as bcr
import matplotlib.pyplot as plt
race = 'DEUTCHLAND'
season = '2024'
pdf_path = f'/home/boris/Documents/matplotlib_exercize/{race}_{season}_MOTO_3/LapChart.pdf'

def sort_by_values_len(dict):
    dict_len= {key: len(value) for key, value in dict.items()}
    import operator
    sorted_key_list = sorted(dict_len.items(), key=operator.itemgetter(1), reverse=True)
    sorted_dict = [{item[0]: dict[item [0]]} for item in sorted_key_list]
    return sorted_dict
drivers = ['Collin VEIJER', 'David MUÑOZ', 'Ivan ORTOLA', 'Ryusei YAMANAKA', 'Joel KELSO',
           'Adrian FERNANDEZ', 'Daniel HOLGADO', 'Nicola CARRARO', 'Stefano NEPA', 'Angel PIQUERAS',
           'David ALONSO', 'Jacob ROULSTONE', 'Filippo FARIOLI', 'Matteo BERTELLE', 'David ALMANSA',
           'Vicente PEREZ', 'Taiyo FURUSATO', 'Riccardo ROSSI', 'Scott OGDEN', 'Luca LUNETTA',
           'Noah DETTWILER', 'Xabi ZURUTUZA', 'Joshua WHATLEY', 'Tatchakorn BUASRI', 'Tatsuki SUZUKI',
           'Joel ESTEBAN', 'Hamad AL-SAHOUTI', 'Jose Antonio RUEDA', 'Arbi ADITAMA']
drivers_colors = ['#081830', '#0581bc', '#e85903', '#e85903', '#0581bc',
                  '#46b2c6', '#6d0406', '#d60057', '#d60057', '#46b2c6',
                  '#01799d', '#6d0406', '#9d9ea0', '#c7b705', '#c7b705', 
                  '#c82305', '#6d6f71', '#00a601', '#e6e8ec', '#9d9ea0',
                  '#00a601', '#c82305', '#e6e8ec', '#6d6f71', '#081830',
                  '#01799d', '#c7b705', '#c82305', '#6d6f71']
drivers_number = ['95', '64', '48', '6', '66',
                  '31', '96', '10', '82', '36',
                  '80', '12', '7', '18', '22', 
                  '21', '72', '54', '19','58',
                  '55', '85', '70', '5', '24', 
                  '78', '71', '99', '93']
ndn =  ['95', '64', '48', '6', '66',
                  '31', '96', '10', '82', '36',
                  '80', '12', '7', '18', '22', 
                  '21', '72', '54', '19','58',
                  '55', '85', '70', '5', '24', 
                  '78', '71', '99', '93']
with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]
    page_width = page.width
    page_height = page.height
    crop_box = (0, 130, page_width, page_height-100)
    cropped_page = page.within_bbox(crop_box)
    text = cropped_page.extract_text()

def solve(text):
    t1_ = ' '.join(str(x) for x in text)
    t = text
    t1 = []
    dn = drivers_number.copy()
    for x in t:
        if x not in drivers_number:
            t1.append(x)
        else:
            dn.remove(x)
    
    combs = []
    for i in range(len(dn)):
        for j in range(len(dn)):
            if i!=j:
                combs.append((f'{dn[i]}{dn[j]}', f'{dn[i]} {dn[j]}'))
    for c in combs:
        for t in t1:
            if c[0] in t:
                t1_ = t1_.replace(c[0], c[1])
    return t1_

all_text = text.split('\n')
start_position = all_text[0].split(' ')[1:]

starting_grid = solve(all_text[1].split(' ')[1:])
starting_grid = starting_grid.split(' ')
num_of_drivers = len(start_position)
drivers_number = ndn

laps_order_dict = {'start_position': start_position,
                   'starting_grid': starting_grid}
laps_order = []

for i in range(2, len(all_text)):
    #all_text[i] = all_text[i].replace('  ', ' ')
    #all_text[i] = solve(all_text[i])
    line = all_text[i].split(' ')
    if line[0].isalpha() and len(line)>2:
        new_line = line[2:]
        new_line = solve(new_line)
        drivers_number = ndn
        new_line = new_line.split(' ')
        if len(new_line) != num_of_drivers:
            add_spaces = num_of_drivers - len(new_line)
            for i in range(add_spaces):
                new_line.append('0')
        laps_order_dict[f'lap {line[1]}'] = new_line
        laps_order.append(new_line)
    elif len(line)>1:
        new_line = line[1:]
        new_line = solve(new_line)
        drivers_number = ndn
        new_line = new_line.split(' ')
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
                to_plot[str(dn)].append(num_of_drivers - (item.index(i)))
to_plot = sort_by_values_len(to_plot)
tp_dict = {}
for tp in to_plot:
    tp_dict[list(tp.items())[0][0]] = list(tp.items())[0][1]
to_plot = tp_dict
not_finish_driver = 0
i = num_of_drivers
for key, item in to_plot.items():
    if len(item) < num_of_laps:
        iters = num_of_laps - len(item)
        for _ in range(iters):
            item.append(i)
    i = i - 1
                
max_x = num_of_laps
max_x_6 = max_x*1.0/6
ticks = [max_x_6*i for i in range(1, 7)]
labels = [f'{int(t)}' for t in ticks]
labels[-1] = f"{num_of_laps}"

plt.figure(figsize=(15,9))
plt.xticks(ticks=ticks, labels=labels, fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)
plt.xlim([-1, num_of_laps+12])
plt.yticks(list(range(1, len(start_position)+1)), labels=[f'{num_of_drivers+1-i}' for i in range(1, len(start_position)+1)], 
                    fontname='Ubuntu', fontweight='bold',
                    fontsize=15,)
plt.ylim([0, len(start_position)+2])
for dn in laps_order_dict['starting_grid']:
    driver_to_plot = str(dn)
    print(driver_to_plot)
    ind_of_number = drivers_number.index((driver_to_plot))
    color_of_driver_to_plot = drivers_colors[ind_of_number]
    drvier = drivers[ind_of_number]
    if len(to_plot[driver_to_plot])>0:
        plt.plot(to_plot[driver_to_plot], color=color_of_driver_to_plot, label=drvier, lw=2)

        plt.tight_layout()

        plt.ylabel('Position', fontname='Ubuntu', fontweight='bold', fontsize=15)
        plt.xlabel('Laps', fontname='Ubuntu', fontweight='bold', fontsize=15)
        plt.text(num_of_laps+1.2, to_plot[driver_to_plot][-1], drvier, fontsize=16,
                    fontname='Ubuntu',
                    color=color_of_driver_to_plot)
        plt.title(f'{race} {season} - Formula 1', fontname='Ubuntu', fontweight='bold', fontsize=15)
#mplcursors.cursor(hover=True)
plt.savefig(f'/home/boris/Documents/matplotlib_exercize/{race}_{season}_MOTO_3/{race}_plot_all.jpg')
#plt.show()