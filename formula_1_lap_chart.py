import pdfplumber
import pandas as pd
import bar_chart_race as bcr
import matplotlib.pyplot as plt
race = 'BELGIA'
season = '2024'
pdf_path = f'/home/boris/Documents/matplotlib_exercize/{race}_{season}_F1/Lap_Chart.pdf'

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
starting_grid = all_text[1].split(' ')[1:]
num_of_drivers = len(start_position)

laps_order_dict = {'start_position': start_position,
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
df_laps_order = pd.DataFrame(laps_order_dict)
#df_laps_order = df_laps_order.set_index('starting_grid')
points = []
first_points = list(range(1,21))
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
points_per_lap['laps'] = [f'lap {i}' for i in range(1, 45)]
points_df = pd.DataFrame(points_per_lap, index=points_per_lap['laps'])
points_df.drop('laps', inplace=True, axis='columns')

#points_df.set_index('laps', inplace=True)
cols = points_df.columns
starting_drivers = []
colors = []
for sg in cols:
    ind = drivers_numbers.index(int(sg))
    starting_drivers.append(drivers[ind])
    colors.append(drivers_colors[ind])
points_df.columns = starting_drivers
bcr.bar_chart_race(
    label_bars=False, 
    df=points_df, 
    title=f'{race}, 2024 Formula 1 Championship Race', 
    orientation='h', 
    sort='desc', 
    n_bars=10, 
    steps_per_period=10, 
    period_length=600,
    filename=f'{race}_{season}_F1/LapChart.mp4', 
    cmap=colors,
    #label_bars=False,
    figsize=(15, 10),
    shared_fontdict={'family': 'Ubuntu', 'weight': 'bold',
                                    'color': 'rebeccapurple'},
    bar_kwargs={'alpha': .8},
    fixed_max=max(points)
)

from moviepy.editor import VideoFileClip, AudioFileClip
import os, random

all_music_files = os.listdir('/home/boris/Documents/matplotlib_exercize/music')
vf = f'/home/boris/Documents/matplotlib_exercize/{race}_{season}_F1/LapChart.mp4'

mf = '/home/boris/Documents/matplotlib_exercize/music/'+random.choice(all_music_files)

vc = VideoFileClip(vf)
mc = AudioFileClip(mf)
fc = vc.set_audio(mc.subclip(0, vc.duration))
fc.write_videofile(f'/home/boris/Documents/matplotlib_exercize/{race}_{season}_F1/LapChart_with_audio.mp4',  codec="libx264", audio_codec="aac")