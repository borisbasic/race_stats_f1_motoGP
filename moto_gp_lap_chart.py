import pdfplumber
import pandas as pd
import bar_chart_race as bcr
import matplotlib.pyplot as plt
race = 'MUGELLO'
season = '2024'
pdf_path = f'/home/boris/Documents/matplotlib_exercize/{race}_{season}/LapChart.pdf'

drivers = ['Francesco BAGNAIA', 'Marc MARQUEZ', 'Marco BEZZECCHI', 'Alex MARQUEZ', 'Enea BASTIANINI', 'Brad BINDER', 
           'Fabio DI GIANNANTONI', 'Miguel OLIVEIRA', 'Pedro ACOSTA', 'Maverick VIÑALES', 'Raul FERNANDEZ',
           'Joan MIR', 'Alex RINS', 'Takaaki NAKAGAMI', 'Fabio QUARTARARO', 'Stefan BRADL', 'Luca MARINI',
           'Augusto FERNANDEZ', 'Jack MILLER', 'Franco MORBIDELLI', 'Lorenzo SAVADORI', 'Jorge MARTIN', 'Johann ZARCO',
           'Aleix ESPARGARO', 'Daniel PEDROSA', 'Pol ESPARGARO']
drivers_colors = ['#cc0001', '#9aadd2', '#e1fa50', '#9aadd2', '#cc0001', '#a44721',
          '#e1fb4f', '#0254b8', '#990525', '#5bb33a', '#0254b8',
          '#fea011', '#072e7e', '#cecece', '#072e7e', '#fea011', '#fea011',
          '#990525', '#a44721', '#8432c5', '#5cb139', '#8432c5', '#cecece',
          '#5bb33a', '#a44721', '#990525']
drivers_numbers = [1, 93, 72, 73, 23, 33,
                   49, 88, 31, 12, 25, 
                   36, 42, 30, 20, 6, 10,
                   37, 43, 21, 32, 89, 5, 
                   41, 26, 44]
with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]
    page_width = page.width
    page_height = page.height
    crop_box = (0, 130, page_width, page_height-100)
    cropped_page = page.within_bbox(crop_box)
    text = cropped_page.extract_text()
    
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

df_laps_order = pd.DataFrame(laps_order_dict)
#df_laps_order = df_laps_order.set_index('starting_grid')
points = []
first_points = list(range(1,num_of_drivers+1))
first_points.reverse()
points_per_lap = {}
for d in drivers_numbers:
    points_per_lap[d] = []

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
    print(sg)
    ind = drivers_numbers.index(int(sg))
    print(drivers[ind])
    print(ind)
    starting_drivers.append(drivers[ind])
    colors.append(drivers_colors[ind])
points_df.columns = starting_drivers
bcr.bar_chart_race(
    df=points_df, 
    title=f'{race}, 2024 MotoGP Championship Race', 
    orientation='h', 
    sort='desc', 
    n_bars=15, 
    steps_per_period=40, 
    period_length=2000,
    filename=f'/home/boris/Documents/matplotlib_exercize/{race}_{season}/LapChart.mp4', 
    cmap=colors,
    label_bars=False,
    figsize=(15, 10),
    shared_fontdict={'family': 'Ubuntu', 'weight': 'bold',
                                    'color': 'rebeccapurple'},
    bar_kwargs={'alpha': .7},
    fixed_max=max(points)
)