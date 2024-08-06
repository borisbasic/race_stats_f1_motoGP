import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import bar_chart_race as bcr
race = 'DEUTCHLAND'
season = '2024'
number_of_gp = 9
plt.style.use('ggplot')

drivers = [ 'Marc MARQUEZ', 'Marco BEZZECCHI', 'Alex MARQUEZ', 'Enea BASTIANINI', 'Brad BINDER', 
           'Fabio DI GIANNANTONI', 'Miguel OLIVEIRA', 'Pedro ACOSTA', 'Maverick VIÑALES', 'Raul FERNANDEZ',
           'Joan MIR', 'Alex RINS', 'Takaaki NAKAGAMI', 'Fabio QUARTARARO', 'Stefan BRADL', 'Luca MARINI',
           'Augusto FERNANDEZ', 'Jack MILLER', 'Franco MORBIDELLI', 'Lorenzo SAVADORI', 'Jorge MARTIN', 'Johann ZARCO',
           'Aleix ESPARGARO', 'Daniel PEDROSA',  'Pol ESPARGARO', 'Francesco BAGNAIA',]
drivers_surname = []
for d in drivers:
    surname = d.split(' ')[1:]
    if len(surname) > 1:
        surname = f'{surname[0]} {surname[1]}'
    else:
        surname = surname[0]
    drivers_surname.append(surname)
drivers_colors = [ '#9aadd2', '#e1fa50', '#9aadd2', '#cc0001', '#a44721',
          '#e1fb4f', '#0254b8', '#990525', '#5bb33a', '#0254b8',
          '#fea011', '#072e7e', '#cecece', '#072e7e', '#fea011', '#fea011',
          '#990525', '#a44721', '#8432c5', '#5cb139', '#8432c5', '#cecece',
          '#5bb33a', '#a44721', '#990525', '#cc0001',]
drivers_colors_matching = ['']
def crop_and_extract_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all = ''
        for page in pdf.pages:
            first_page = page
            page_width = first_page.width
            page_height = first_page.height

            # Crop the left half of the page
            crop_box = (0, 0, page_width, page_height-100)
            cropped_page = first_page.within_bbox(crop_box)

            crop_box_ = (page_width / 2 + 15, 0, page_width, page_height-100)
            cropped_page_ = first_page.within_bbox(crop_box_) 
            # Extract text from the cropped region
            text = cropped_page.extract_text()
            text_ = cropped_page_.extract_text()
            all = all + text 
    return all

pdf_path = f"/home/boris/Documents/matplotlib_exercize/{race}_{season}/worldstanding.pdf"
text = crop_and_extract_text(pdf_path)
all_data = text.split('\n')
drivers_dict = {}
list_len = 0
points = 0
for i in range(len(all_data)):
    for ds in drivers_surname:
        if ds in all_data[i]:
            if all_data[i].split(' ')[0] == '1':
                all_data[i] = all_data[i].replace('-', '0')
                d1 = all_data[i].split(' ')
                d2 = all_data[i+1].split(' ')
                l1 = d1[3:]
                res = [eval(i) for i in l1]
                drivers_dict[f'{d2[0]} {d1[1]}']= res
                if max(res) > points:
                    points = max(res)
            else:
                all_data[i] = all_data[i].replace('-', '0')
                all_data[i] = all_data[i].replace(ds, '')
                d1 = all_data[i].split(' ')
                d2 = all_data[i+1].split(' ')
                l1 = d1[5:]
                res = [eval(i) for i in l1]
                drivers_dict[f'{d2[0]} {ds}']= res
                list_len = len(d1[5:])
                if max(res) > points:
                    points = max(res)
    if all_data[i].startswith('PointsLeader'):
        drivers_dict['races'] = all_data[i].split(' ')[2:]
drivers_dict['races'] = drivers_dict['races'][:number_of_gp]

standings_df = pd.DataFrame(drivers_dict, index=drivers_dict['races'])
standings_df.drop(columns=['races'], inplace=True)
standings_df = standings_df.cumsum()

cols = standings_df.columns
starting_drivers = []
colors = []
for sg in cols:
    ind = drivers.index((sg))
    starting_drivers.append(drivers[ind])
    colors.append(drivers_colors[ind])

bcr.bar_chart_race(
    df=standings_df, 
    title=f'After {race}, 2024 MotoGP Championship Race', 
    orientation='h', 
    sort='desc', 
    n_bars=12, 
    steps_per_period=40, 
    period_length=2000,
    filename=f'/home/boris/Documents/matplotlib_exercize/{race}_{season}/World_standings.mp4', 
    cmap=colors,
    figsize=(15, 10),
    shared_fontdict={'family': 'Ubuntu', 'weight': 'bold',
                                    'color': 'rebeccapurple'},
    bar_kwargs={'alpha': .7},
    fixed_max=points
)

from moviepy.editor import VideoFileClip, AudioFileClip
import os, random

all_music_files = os.listdir('/home/boris/Documents/matplotlib_exercize/music')
vf = f'/home/boris/Documents/matplotlib_exercize/{race}_{season}/World_standings.mp4'

mf = '/home/boris/Documents/matplotlib_exercize/music/'+random.choice(all_music_files)

vc = VideoFileClip(vf)
mc = AudioFileClip(mf)
fc = vc.set_audio(mc.subclip(0, vc.duration))
fc.write_videofile(f'/home/boris/Documents/matplotlib_exercize/{race}_{season}/World_standings_with_audio.mp4',  codec="libx264", audio_codec="aac")