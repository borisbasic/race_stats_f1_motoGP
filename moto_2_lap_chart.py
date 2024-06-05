import pdfplumber
import pandas as pd
import bar_chart_race as bcr
import matplotlib.pyplot as plt
race = 'MUGELLO'
season = '2024'
pdf_path = f'/home/boris/Documents/matplotlib_exercize/{race}_{season}_MOTO_2/LapChart.pdf'

drivers = ['Fermin ALDEGUER', 'Joe ROBERTS', 'Manuel GONZALEZ', 'Sergio GARCIA', 
           'Albert ARENAS', 'Ai OGURA', 'Tony ARBOLINO', 'Jeremy ALCOBA', 'Celestino VIETTI', 
           'Somkiat CHANTRA', 'Filip SALAC', 'Izan GUEVARA', 'Zonta VD GOORBE', 'Deniz ÖNCÜ',
           'Matteo FERRARI', 'Mario AJI', 'Xavi CARDELUS', 'Jorge NAVARRO', 
           'Darryn BINDER', 'Xavier ARTIGAS', 'Jaume MASIA', 'Jake DIXON', 'Alonso LOPEZ',
           'Marcos RAMIREZ', 'Alex ESCRIG', 'Diogo MOREIRA', 'Barry BALTUS',
           'Dennis FOGGIA', 'Senna AGIUS', 'Bo BENDSNEYDER', 'Ayumu SASAKI', 'Aron CANET', 'Daniel MUÑOZ',
           'Mattia PASINI']
drivers_colors = ['#ffcf49', '#011663','#6475a6', '#fa2701', 
                  '#6475a6', '#fa2701', '#291515', '#011c53', '#e84003',
                  '#635f34', '#291515', '#017da3', '#cccbce', '#e84003',
                  '#6475a6', '#635f34', '#99999c', '#048d71',
                  '#18243b', '#8db9b5', '#7f0809', '#017da3', '#ffcf49',
                  '#011663', '#8db9b5', '#082a51', '#cccbce',
                  '#082a51', '#18243b', '#7f0809', '#011c53', '#99999c', '#7f0809',
                  '#991111']
drivers_number = ['54', '16', '18', '3', 
                  '75', '79', '14', '52', '13',
                  '35', '12', '28', '84', '53', 
                  '23', '34', '20', '9',
                  '15', '43', '5', '96', '21', 
                  '24', '11', '10', '7',
                  '71', '81', '64', '22', '44', '17',
                  '19']
ndn = ['54', '16', '18', '3', 
                  '75', '79', '14', '52', '13',
                  '35', '12', '28', '84', '53', 
                  '23', '34', '20', '9',
                  '15', '43', '5', '96', '21', 
                  '24', '11', '10', '7',
                  '71', '81', '64', '22', '44', '17',
                  '19']

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

df_laps_order = pd.DataFrame(laps_order_dict)
#df_laps_order = df_laps_order.set_index('starting_grid')
points = []
first_points = list(range(1,num_of_drivers+1))
first_points.reverse()
points_per_lap = {}
for d in drivers_number:
    points_per_lap[int(d)] = []
for i in range(len(starting_grid)):
    last_position = int(start_position[i])
    for lap in laps_order:
        if starting_grid[i] in lap:
            ind = lap.index(starting_grid[i]) + 1
            if ind > int(last_position):
                first_points[i] = first_points[i] + 2 - (ind-last_position)
                last_position = ind 
                points_per_lap[int(starting_grid[i])].append(first_points[i])
            elif ind < int(last_position):
                first_points[i] = first_points[i] + 2 + (last_position - ind)
                points_per_lap[int(starting_grid[i])].append(first_points[i])
                last_position = ind
            else:
                first_points[i] = first_points[i] + 2
                points_per_lap[int(starting_grid[i])].append(first_points[i])
        else:
            points_per_lap[int(starting_grid[i])].append(first_points[i])
            
    
    points.append(first_points[i])
for key, items in points_per_lap.copy().items():
    if len(items) == 0:
        del points_per_lap[key]
points_per_lap['laps'] = [f'lap {i}' for i in range(1, len(laps_order_dict)-1)]
points_df = pd.DataFrame(points_per_lap, index=points_per_lap['laps'])
points_df.drop('laps', inplace=True, axis='columns')

#points_df.set_index('laps', inplace=True)
cols = points_df.columns
starting_drivers = []
colors = []
for sg in cols:
    ind = drivers_number.index(str(sg))
    starting_drivers.append(drivers[ind])
    colors.append(drivers_colors[ind])
points_df.columns = starting_drivers
bcr.bar_chart_race(
    df=points_df, 
    title=f'{race}, 2024 Moto2 Championship Race', 
    orientation='h', 
    sort='desc', 
    n_bars=15, 
    steps_per_period=40, 
    period_length=2000,
    filename=f'/home/boris/Documents/matplotlib_exercize/{race}_{season}_MOTO_2/LapChart_Moto_2.mp4', 
    cmap=colors,
    label_bars=False,
    figsize=(15, 10),
    shared_fontdict={'family': 'Ubuntu', 'weight': 'bold',
                                    'color': 'rebeccapurple'},
    bar_kwargs={'alpha': .7},
    fixed_max=max(points)
)