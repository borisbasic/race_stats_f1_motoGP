import pdfplumber
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as image
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
#plt.style.use('ggplot')


race = 'BELGIA'
season = '2024'

if not os.path.isdir(f'{race}_{season}_F1/{race}_{season}_Analysis'):
    os.mkdir(f'{race}_{season}_F1/{race}_{season}_Analysis')

drivers = ['Max VERSTAPPEN', 'Sergio PEREZ', 'Charles LECLERC', 'Lando NORRIS', 'Carlos SAINZ',
            'Oscar PIASTRI', 'George RUSSEL', 'Fernando ALONSO', 'Lewis HAMILTON', 'Yuki TSUNODA', 'Lance STROLL', 
           'Oliver BEARMAN', 'Nico HULKENBERG', 'Daniel RICCIARDO', 'Esteban OCON', 'Kevin MAGNUSSEN', 
           'Alexander ALBON', 'ZHOU Guanyu', 'Pierre GASLY', 'Valtteri BOTTAS', 'Logan SARGEANT']
drivers_colors = ['#3671c6', '#3671c6', '#d92e37', '#c15206', '#d92e37',
                  '#c15206', '#23dbbd', '#037c78', '#23dbbd', '#6692ff', '#037c78',
                  '#d92e37', '#b6babd', '#6692ff', '#0093cc', '#b6babd',
                  '#64c4ff', '#76c97b', '#0093cc', '#76c97b', '#64c4ff']
drivers_numbers = [1, 11, 16, 4, 55,
                   81,  63, 14, 44, 22, 18,
                   12, 27, 3, 31, 20,
                   23, 24, 10, 77, 2]

pdf_path = f'/home/boris/Documents/matplotlib_exercize/{race}_{season}_F1/Qualification.pdf'
with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]
    page_width = page.width
    page_height = page.height
    crop_box = (0, 164, page_width, page_height-70)
    cropped_page = page.within_bbox(crop_box)
    text = cropped_page.extract_text() 

first_ten = text.split('\n')[1:11]
last_ten = text.split('\n')[11:21]
fig, ax = plt.subplots(figsize = (8, 14), constrained_layout=True, facecolor='#dee2e6')
ax.set_facecolor('#dee2e6')
i=1
j=0.93
name = ''
color = ''
for ft in first_ten:
    car = ft.split(':')[0]
    for d in drivers:
        if d in car:
            car = car.split(d)[1][1:-2].strip().replace(' ', '_')
            name = d
            ind_of_driver = drivers.index(name)
            color = drivers_colors[ind_of_driver]
            break
    time = ft.split(' ')[-3]
    file = f'/home/boris/Documents/matplotlib_exercize/formula_1_images/{car}-removebg-preview.png'
    alpine_logo = image.imread(file)

    imagebox = OffsetImage(alpine_logo, zoom=0.5, )
    if i%2 == 1:
        ab = AnnotationBbox(imagebox, (0.2, j), bboxprops =dict(edgecolor='white'), frameon=False)
        ax.add_artist(ab)
        name_time = f"{i}. {name.split(' ')[0]}\n{name.split(' ')[1]}\n{time}"
        plt.text(0.3, j, name_time, fontsize=16,
                    fontname='FreeSans', color=color, fontweight='bold',
                    #bbox=dict(boxstyle='round', edgecolor='none', facecolor='white')
                    )
    else:
        ab = AnnotationBbox(imagebox, (0.7, j), bboxprops =dict(edgecolor='white'), frameon=False)
        ax.add_artist(ab)
        name_time = f"{i}. {name.split(' ')[0]}\n{name.split(' ')[1]}\n{time}"
        plt.text(0.8, j, name_time, fontsize=16, 
                    fontname='FreeSans', color=color, fontweight='bold',
                    #bbox=dict(boxstyle='round', edgecolor='none', facecolor='white')
                    )
    j = j - 0.1
    i = i + 1

plt.axvline(0.5, color='white', linestyle='--', linewidth=9)
plt.axvline(0.05, color='white', linestyle='-', linewidth=9)
plt.axvline(0.95, color='white', linestyle='-', linewidth=9)
plt.axis('off')
plt.title(f'{race} Qualifying Session', fontname='Ubuntu', fontweight='bold', fontsize=21)
plt.savefig(f'{race}_{season}_F1/ten_first_qualify_order.jpg')


fig, ax = plt.subplots(figsize = (8, 14), constrained_layout=True, facecolor='#dee2e6')
ax.set_facecolor('#dee2e6')
i=1
j=0.93
name = ''
color = ''
for ft in last_ten:
    car = ft.split(':')[0]
    print(car)
    for d in drivers:
        if d in car:
            #print(car)
            car = car.split(d)[1][1:-2].strip().replace(' ', '_')
            name = d
            ind_of_driver = drivers.index(name)
            color = drivers_colors[ind_of_driver]
            break
    if int(ft.split(' ')[0]) > 15:
        time = ft.split(' ')[-4]
    else:
        time = ft.split(' ')[-3]
    file = f'/home/boris/Documents/matplotlib_exercize/formula_1_images/{car}-removebg-preview.png'
    alpine_logo = image.imread(file)

    imagebox = OffsetImage(alpine_logo, zoom=0.5, )
    if i%2 == 1:
        ab = AnnotationBbox(imagebox, (0.2, j), bboxprops =dict(edgecolor='white'), frameon=False)
        ax.add_artist(ab)
        name_time = f"{i+10}. {name.split(' ')[0]}\n{name.split(' ')[1]}\n{time}"
        plt.text(0.3, j, name_time, fontsize=16,
                    fontname='FreeSans', color=color, fontweight='bold',
                    #bbox=dict(boxstyle='round', edgecolor='none', facecolor='white')
                    )
    else:
        ab = AnnotationBbox(imagebox, (0.7, j), bboxprops =dict(edgecolor='white'), frameon=False)
        ax.add_artist(ab)
        name_time = f"{i+10}. {name.split(' ')[0]}\n{name.split(' ')[1]}\n{time}"
        plt.text(0.8, j, name_time, fontsize=16, 
                    fontname='FreeSans', color=color, fontweight='bold',
                    #bbox=dict(boxstyle='round', edgecolor='none', facecolor='white')
                    )
    j = j - 0.1
    i = i + 1

plt.axvline(0.5, color='white', linestyle='--', linewidth=9)
plt.axvline(0.05, color='white', linestyle='-', linewidth=9)
plt.axvline(0.95, color='white', linestyle='-', linewidth=9)
plt.axis('off')
plt.title(f'{race} Qualifying Session', fontname='Ubuntu', fontweight='bold', fontsize=21)
plt.savefig(f'{race}_{season}_F1/ten_last_qualify_order.jpg')
 

