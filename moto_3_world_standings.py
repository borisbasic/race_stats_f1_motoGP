import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import bar_chart_race as bcr
plt.style.use('ggplot')
number_of_gp = 9
race = 'DEUTCHLAND'
season = '2024'
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
nd = []
for d in drivers:
    name = d.split(' ')[0]
    surname = d.split(' ')[1]
    nd.append(f'{surname} {name}')

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

            crop_box_ = (page_width / 2 + 15, 0, page_width, page_height)
            cropped_page_ = first_page.within_bbox(crop_box_) 
            # Extract text from the cropped region
            text = cropped_page.extract_text()
            text_ = cropped_page_.extract_text()
            all = all + text 
    return all

pdf_path = f"/home/boris/Documents/matplotlib_exercize/{race}_{season}_MOTO_3/worldstanding.pdf"
text = crop_and_extract_text(pdf_path)
all_data = text.split('\n')
drivers_dict = {}
list_len = 0
points = 0
for i in range(len(all_data)):
    for ds in nd:
        if ds in all_data[i]:
            if all_data[i].split(' ')[0] == '1':
                all_data[i] = all_data[i].replace('-', '0')
                all_data[i] = all_data[i].replace(ds, '')
                d1 = all_data[i].split(' ')
                l1 = d1[4:(number_of_gp+4)]
                res = [eval(i) for i in l1]
                drivers_dict[f'{ds}']= res

                list_len = 4
                if max(res) > points:
                    points = max(res)
            else:
                all_data[i] = all_data[i].replace('-', '0')
                all_data[i] = all_data[i].replace(ds, '')
                d1 = all_data[i].split(' ')
                l1 = d1[6:(number_of_gp+6)]
                l1_ = []
                x1 = ''
                for x in l1:
                    for y in x:
                        if y.isnumeric():
                            x1 = x1 + y
                    l1_.append(x1)
                    x1 = ''
                res = [eval(i) for i in l1_]
                drivers_dict[f'{ds}']= res
                if max(res) > points:
                    points = max(res)
    if all_data[i].startswith('Points LeaderPrevious'):
        drivers_dict['races'] = all_data[i].split(' ')[2:]
drivers_dict['races'] = drivers_dict['races'][:number_of_gp]
standings_df = pd.DataFrame(drivers_dict, index=drivers_dict['races'])
standings_df.drop(columns=['races'], inplace=True)
standings_df = standings_df.cumsum()
cols = standings_df.columns
starting_drivers = []
colors = []
for sg in cols:
    ind = nd.index((sg))
    starting_drivers.append(drivers[ind])
    colors.append(drivers_colors[ind])

bcr.bar_chart_race(
    df=standings_df, 
    title=f'After {race}, 2024 Moto3 Championship Race', 
    orientation='h', 
    sort='desc', 
    n_bars=12, 
    steps_per_period=40, 
    period_length=2000,
    filename=f'/home/boris/Documents/matplotlib_exercize/{race}_{season}_MOTO_3/World_standings.mp4', 
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
vf = f'/home/boris/Documents/matplotlib_exercize/{race}_{season}_MOTO_3/World_standings.mp4'

mf = '/home/boris/Documents/matplotlib_exercize/music/'+random.choice(all_music_files)

vc = VideoFileClip(vf)
mc = AudioFileClip(mf)
fc = vc.set_audio(mc.subclip(0, vc.duration))
fc.write_videofile(f'/home/boris/Documents/matplotlib_exercize/{race}_{season}_MOTO_3/World_standings_with_audio.mp4',  codec="libx264", audio_codec="aac")