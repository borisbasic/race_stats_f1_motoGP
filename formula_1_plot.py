import pdfplumber
import pandas as pd
import bar_chart_race as bcr
import matplotlib.pyplot as plt
race = 'BELGIA'
season = '2024'
pdf_path = f'/home/boris/Documents/matplotlib_exercize/{race}_{season}_F1/Lap_Chart.pdf'

def sort_by_values_len(dict):
    dict_len= {key: len(value) for key, value in dict.items()}
    import operator
    sorted_key_list = sorted(dict_len.items(), key=operator.itemgetter(1), reverse=True)
    sorted_dict = [{item[0]: dict[item [0]]} for item in sorted_key_list]
    return sorted_dict

drivers = ['Max VERSTAPPEN', 'Sergio PEREZ', 'Charles LECLERC', 'Lando NORRIS', 'Carlos SAINZ',
            'Oscar PIASTRI', 'George RUSSEL', 'Fernando ALONSO', 'Lewis HAMILTON', 'Yuki TSUNODA', 'Lance STROLL', 
           'Oliver BEARMAN', 'Nico HULKENBERG', 'Daniel RICCIARDO', 'Esteban OCON', 'Kevin MAGNUSSEN', 
           'Alexander ALBON', 'Guanyu ZHOU', 'Pierre GASLY', 'Valterri BOTTAS', 'Logan SARGEANT']
drivers_colors = ['#3671c6', '#3671c6', '#d92e37', '#c15206', '#d92e37',
                  '#c15206', '#27f4d2', '#037c78', '#27f4d2', '#6692ff', '#037c78',
                  '#d92e37', '#b6babd', '#6692ff', '#0093cc', '#b6babd',
                  '#64c4ff', '#76c97b', '#0093cc', '#76c97b', '#64c4ff']
drivers_numbers = [1, 11, 16, 4, 55,
                   81,  63, 14, 44, 22, 18,
                   12, 27, 3, 31, 20,
                   23, 24, 10, 77, 2]
with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]
    #page_1 = pdf.pages[1]
    page_width = page.width
    page_height = page.height
    crop_box = (0, 164, page_width, page_height-70)
    cropped_page = page.within_bbox(crop_box)
    #cropped_page_1 = page_1.within_bbox(crop_box)
    text = cropped_page.extract_text() +'\n'#+ cropped_page_1.extract_text()
    
all_text = text.split('\n')
start_position = all_text[0].split(' ')[1:]
sp = [int(s1) for s1 in start_position]
starting_grid = all_text[1].split(' ')[1:]
num_of_drivers = len(start_position)

laps_order_dict = {
                   'starting_grid': starting_grid}
laps_order = []
for i in range(2, len(all_text)):
    line = all_text[i].split(' ')
    if line[0]=='LAP' and len(line)>2:
        new_line = line[2:]
        if len(new_line) != num_of_drivers:
            add_spaces = num_of_drivers - len(new_line)
            for i in range(add_spaces):
                new_line.append('0')
        laps_order_dict[f'lap {line[1]}'] = new_line
        laps_order.append(new_line)
    #elif len(line)>1:
    #    new_line = line[1:]
    #    if len(new_line) != num_of_drivers:
    #        add_spaces = num_of_drivers - len(new_line)
    #        for i in range(add_spaces):
    #            new_line.append('0')
    #    laps_order_dict[f'lap {line[0]}'] = new_line
    #    laps_order.append(new_line)
num_of_laps = len(laps_order)
to_plot = {}
for dn in laps_order_dict['starting_grid']:
    to_plot[str(dn)] = []
    for key, item in laps_order_dict.items():
        for i in item:
            if str(dn) == i:
                to_plot[str(dn)].append(20 - (item.index(i)))
to_plot = sort_by_values_len(to_plot)
tp_dict = {}
for tp in to_plot:
    tp_dict[list(tp.items())[0][0]] = list(tp.items())[0][1]
to_plot = tp_dict
not_finish_driver = 0
i = 20
for key, item in to_plot.items():
    if len(item) < num_of_laps:
        iters = num_of_laps - len(item)
        for _ in range(iters):
            item.append(i)
    i = i - 1
print(to_plot)
                
max_x = num_of_laps
max_x_6 = max_x*1.0/6
ticks = [max_x_6*i for i in range(1, 7)]
labels = [f'{int(t)}' for t in ticks]
labels[-1] = f"{num_of_laps}"

plt.figure(figsize=(15,9))
plt.xticks(ticks=ticks, labels=labels, fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)
plt.xlim([-1, num_of_laps+12])
plt.yticks(list(range(1, len(start_position)+1)), labels=[f'{21-i}' for i in range(1, len(start_position)+1)], 
                    fontname='Ubuntu', fontweight='bold',
                    fontsize=15,)
plt.ylim([0, len(start_position)+2])
for dn in laps_order_dict['starting_grid']:
    driver_to_plot = str(dn)
    ind_of_number = drivers_numbers.index(int(driver_to_plot))
    color_of_driver_to_plot = drivers_colors[ind_of_number]
    drvier = drivers[ind_of_number]
    if len(to_plot[driver_to_plot])>0:
        plt.plot(to_plot[driver_to_plot], color=color_of_driver_to_plot, label=drvier, lw=2)

        plt.tight_layout()

        plt.ylabel('Position', fontname='Ubuntu', fontweight='bold', fontsize=15)
        plt.xlabel('Laps', fontname='Ubuntu', fontweight='bold', fontsize=15)
        plt.text(num_of_laps+1, to_plot[driver_to_plot][-1], drvier, fontsize=16,
                    fontname='Ubuntu',
                    color=color_of_driver_to_plot)
        plt.title(f'{race} {season} - Formula 1', fontname='Ubuntu', fontweight='bold', fontsize=15)
#mplcursors.cursor(hover=True)
plt.savefig(f'/home/boris/Documents/matplotlib_exercize/{race}_{season}_F1/plot_all.jpg')
#plt.show()