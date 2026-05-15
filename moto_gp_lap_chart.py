import pdfplumber
import pandas as pd
import bar_chart_race as bcr
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip
from moviepy.audio.fx.all import audio_fadeout
import os, random
race = 'ASSEN'
season = '2024'
pdf_path = f'/home/boris/Documents/matplotlib_exercize/moto2mot3motogp_old_scripts/{race}_{season}/LapChart.pdf'
base_path = f'/home/boris/Documents/matplotlib_exercize/moto2mot3motogp_old_scripts/{race}_{season}'

drivers = ['Francesco BAGNAIA', 'Marc MARQUEZ', 'Marco BEZZECCHI', 'Alex MARQUEZ', 'Enea BASTIANINI', 'Brad BINDER', 
           'Fabio DI GIANNANTONI', 'Miguel OLIVEIRA', 'Pedro ACOSTA', 'Maverick VIÑALES', 'Raul FERNANDEZ',
           'Joan MIR', 'Alex RINS', 'Takaaki NAKAGAMI', 'Fabio QUARTARARO', 'Stefan BRADL', 'Luca MARINI',
           'Augusto FERNANDEZ', 'Jack MILLER', 'Franco MORBIDELLI', 'Lorenzo SAVADORI', 'Jorge MARTIN', 'Johann ZARCO',
           'Aleix ESPARGARO', 'Daniel PEDROSA', 'Pol ESPARGARO', 'Remy GARDNER']
drivers_colors = ['#cc0001', '#9aadd2', '#e1fa50', '#9aadd2', '#cc0001', '#a44721',
          '#e1fb4f', '#0254b8', '#990525', '#5bb33a', '#0254b8',
          '#fea011', '#072e7e', '#cecece', '#072e7e', '#fea011', '#fea011',
          '#990525', '#a44721', '#8432c5', '#5cb139', '#8432c5', '#cecece',
          '#5bb33a', '#a44721', '#990525', '#072e7e']
drivers_numbers = [1, 93, 72, 73, 23, 33,
                   49, 88, 31, 12, 25, 
                   36, 42, 30, 20, 6, 10,
                   37, 43, 21, 32, 89, 5, 
                   41, 26, 44, 87]
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
def create_static_frame(text, subtitle, filename, color='#ffffff'):
    fig, ax = plt.subplots(figsize=(10, 16), facecolor='#050505')
    ax.set_facecolor('#050505')
    
    ax.text(0.5, 0.55, text, color=color, fontsize=55, ha='center', va='center', weight='bold', family='Ubuntu')
    ax.text(0.5, 0.40, subtitle, color='gray', fontsize=35, ha='center', va='center', family='Ubuntu')
    
    ax.axis('off')
    plt.savefig(filename, dpi=100, facecolor=fig.get_facecolor(), pad_inches=0.5)
    plt.close()

winner_name = points_df.iloc[-1].idxmax()

intro_img = f'{base_path}/intro.png'
outro_img = f'{base_path}/outro.png'
create_static_frame(f"{race} {season}", "MotoGP Lap Chart Analysis", intro_img)
create_static_frame("RACE WINNER", winner_name.upper(), outro_img, color='#f5e642')

main_video_path = f'{base_path}/LapChart_raw.mp4'

plt.rcParams['figure.subplot.left'] = 0.2  
plt.rcParams['figure.subplot.right'] = 0.95

bcr.bar_chart_race(
    df=points_df, 
    title=f'{race}, {season} MotoGP Championship Race', 
    orientation='h', 
    sort='desc', 
    n_bars=15, 
    steps_per_period=40, 
    period_length=1000,
    filename=f'{main_video_path}', 
    cmap=colors,
    label_bars=False,
    figsize=(10, 16),
    shared_fontdict={'family': 'Ubuntu', 'weight': 'bold',
                                    'color': 'rebeccapurple'},
    bar_kwargs={'alpha': .9},
    fixed_max=max(points)
)

all_music_files = [f for f in os.listdir('/home/boris/Documents/matplotlib_exercize/music') if f.endswith('.mp3')]
mf = '/home/boris/Documents/matplotlib_exercize/music/' + random.choice(all_music_files)

intro_clip = ImageClip(intro_img).set_duration(3)
video_clip = VideoFileClip(main_video_path)
outro_clip = ImageClip(outro_img).set_duration(4)

final_video = concatenate_videoclips([intro_clip, video_clip, outro_clip], method="compose")


def create_watermark_img(filename):
    fig, ax = plt.subplots(figsize=(4, 1), facecolor='none')
    # Transparentna pozadina
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    ax.text(0.5, 0.5, "motoslicks.com", color='white', alpha=0.5, 
            fontsize=20, ha='center', va='center', weight='bold')
    ax.axis('off')
    plt.savefig(filename, transparent=True, dpi=100)
    plt.close()

watermark_path = f'{base_path}/wm.png'
create_watermark_img(watermark_path)

# 2. Učitaj kao ImageClip i nalepi
watermark = ImageClip(watermark_path).set_duration(final_video.duration)
watermark = watermark.set_position(("right", "bottom")).margin(right=20, bottom=20, opacity=0)

final_video_ready = CompositeVideoClip([final_video, watermark])

mc = AudioFileClip(mf)
temp_audio = mc.subclip(0, final_video_ready.duration)

from moviepy.audio.fx.all import audio_fadeout
final_audio = audio_fadeout(temp_audio, 2)

final_video_ready = final_video_ready.set_audio(final_audio)

final_output = f'{base_path}/MotoSlicks_Branded_Analysis.mp4'
final_video_ready.write_videofile(final_output, codec="libx264", audio_codec="aac", fps=24)

print(f"Brendirani video spreman na: {final_output}")

os.remove(intro_img)
os.remove(outro_img)

print(f"Video uspešno generisan: {final_output}")