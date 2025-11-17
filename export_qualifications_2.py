
import pandas as pd
import matplotlib.pyplot as plt
import os
import pdfplumber
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
img_moto = '/home/boris/Downloads/depositphotos_54805247-stock-illustration-moto-race-removebg-preview.png'
img_moto_1 = '/home/boris/Downloads/depositphotos_54805235-stock-illustration-moto-race-with-flag-removebg-preview.png'
background = '/home/boris/Downloads/finish-line-racing-background-top-600nw-2470365807.jpg'
class_moto = os.listdir('/home/boris/Documents/matplotlib_exercize/moto_pdfs')

images_moto = '/home/boris/Documents/motogp_api/images'

for cm in class_moto:
    important_things_csv = '/home/boris/Documents/matplotlib_exercize/done/qualifications_2.csv'
    important_things_csv = pd.read_csv(important_things_csv)
    important_races = important_things_csv['race'].tolist()
    important_years = important_things_csv['year'].tolist()
    important_classes = important_things_csv['class'].tolist()
    important_done = important_things_csv['is_done'].tolist()
    if cm not in ['motogp', 'moto2', 'moto3']:
        continue
    year = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}')
    for y in year:
        if y not in ['2025']:
            continue
        list_of_year = os.listdir(f'{images_moto}/{cm}')
        if y not in list_of_year:
            os.mkdir(f'{images_moto}/{cm}/{y}')
        if not os.path.isdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}'):
            continue
        races = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}') 
        for r in races:
            dones = important_things_csv[(important_things_csv['race'] == r) & (important_things_csv['year'] == int(y)) & (important_things_csv['class'] == cm)]['is_done'].tolist()
            
            if 'yes' in dones:
                continue
            list_of_races = os.listdir(f'{images_moto}/{cm}/{y}')
            important_races.append(r)
            important_years.append(y)
            important_classes.append(cm)
            if r not in list_of_races:
                os.mkdir(f'{images_moto}/{cm}/{y}/{r}')
            seasion = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}')
            for s in seasion:
                if s not in ['q2']:
                    continue
                list_of_seasion = os.listdir(f'{images_moto}/{cm}/{y}/{r}')
                if s not in list_of_seasion:
                    os.mkdir(f'{images_moto}/{cm}/{y}/{r}/{s}')
                if not os.path.exists(f"/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/QualifyingResults.pdf"):
                    continue
                entry = f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/rac/entry.csv'
                entry = pd.read_csv(entry)
                bikes = '/home/boris/Documents/matplotlib_exercize/all_drivers_with_colors.csv'
                bikes = pd.read_csv(bikes)
                drivers_ = []
                drivers_colors = []
                drivers_numbers = []
                dri = []
                dr_c = []
                dri_n = []
                dri_time = []
                dri_team = []
                dri_milis = []
                
                a_df_r = pd.DataFrame()
                time_dict = {}
                num_of_lap = 0
                pdf_path = f"/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/QualifyingResults.pdf"
                with pdfplumber.open(pdf_path) as pdf:
                    page = pdf.pages[0]
                    page_width = page.width
                    page_height = page.height
                    crop_box = (0, 130, page_width, page_height-100)
                    cropped_page = page.within_bbox(crop_box)
                    text = cropped_page.extract_text()
                    
                all_text = text.split('\n') 
                
                cond = False
                for at in all_text:
                    line = at.split(' ')
                    if line[0].isnumeric():
                        if f'{line[3]} {line[2]}' == 'DI Fabio':
                            dri.append(f'{line[3]} {line[4]} {line[2]}')
                        elif f'{line[3]} {line[2]}' == 'Antonio Jose':
                            dri.append(f'{line[4]} {line[2]} {line[3]}')
                        elif f'{line[3]} {line[2]}' == 'VD Zonta':
                            dri.append(f'{line[3]} {line[4]} {line[2]}')
                        else:
                            dri.append(f'{line[3]} {line[2]}')
                        for l in line:
                            if "'" in l:
                                if l[0].isnumeric():
                                    dri_time.append(l)
                                    mins = l.split("'")[0]
                                    seconds = l.split("'")[1].split('.')[0]
                                    millis = l.split("'")[1].split('.')[1]
                                    miliss_total = int(mins)*60000 + int(seconds)*1000 + int(millis)
                                    dri_milis.append(miliss_total)
                                    cond = True
                        if not cond:
                            dri_time.append('No Time')
                        cond = False
                for d in dri:
                    try:
                        bike = entry[entry['rider'] == f'{d} ']['team'].values[0]
                        dri_team.append(bike.strip())
                        color = bikes[(bikes['team']==bike.strip()) & (bikes['year']==int(y))]['hex_color'].values[0]
                        dr_c.append(color)
                    except:
                        dr_c.append("#693B116C")
                
                dri_dict = {'driver': dri, 'time': dri_time, 'team': dri_team, 'color': dr_c}
                fig, ax = plt.subplots(figsize =(12, 9), facecolor="#eaeaea7b")

                ticks = []
                ticksx = [0, 1, 2, 3, 4]
                for nor in range(1, 11):
                    ticks.append(f'{nor}.')
                ticks.append('')
                ax.yaxis.set_ticks(list(range(1, 12)), labels=ticks, 
                                fontname='Ubuntu', fontweight='bold',
                                fontsize=15,)

                ax.xaxis.set_ticks(ticks=ticksx, labels=[f'{i}' for i in ticksx], fontweight='bold', fontname='Ubuntu',
                                fontsize=15,)
                ax.set_facecolor("#eaeaea7b")
                    
                img = mpimg.imread(img_moto)
                image_box = OffsetImage(img, zoom=0.1)
                img = mpimg.imread(img_moto_1)
                image_box_1 = OffsetImage(img, zoom=0.1)
                num_of_dri = 0
                if len(dri) > 26:
                    minus = 0.9
                elif len(dri) > 23:
                    minus = 0.8
                elif len(dri) > 20:
                    minus = 0.75
                
                ax.axis('off')
                bg = mpimg.imread(background)
                plt.imshow(bg, extent=[-0.5, 4.5, -0.5, 10+1.5], aspect='auto', alpha=0.6)
                num_of_dri = 0
                max_milis = dri_milis[0]
                dis = 0.3
                for i in range(1, 11):
                    xy = (1+ dis + (-max_milis + dri_milis[num_of_dri])/1000, i)
                    ab = AnnotationBbox(image_box, xy, frameon=True, bboxprops=dict(facecolor=dr_c[num_of_dri], alpha=0.8, edgecolor='none', boxstyle='round,pad=0.3'))
                    ax.add_artist(ab)
                    ax.text(1.1+ dis + (-max_milis + dri_milis[num_of_dri])/1000 + 0.1, i-0.19, 
                            f'{dri[num_of_dri]} \n {dri_time[num_of_dri]} \n +{(-max_milis + dri_milis[num_of_dri])/1000}', 
                            fontsize=11, fontweight='bold', fontname='Ubuntu', color=dr_c[num_of_dri], ha='left',
                              bbox=dict(
                                    facecolor='#FFFFFF',
                                    edgecolor='none',  
                                    boxstyle='round,pad=0.1'
                                ))
                    num_of_dri = num_of_dri + 1
                if len(r) > 20:
                    r1 = r.split(' ')
                    r11 = r1[:len(r1)//2]
                    r12 = r1[len(r1)//2:]
                    r3 = ' '.join(r11) + '\n' + ' '.join(r12)
                else:
                    r3 = r
                plt.text(3.9, 2, f"{cm.upper()} - {r3} \n QUALIFICATION ", rotation=90, ha='center', fontweight='bold', fontsize=25, color="#1110103B", clip_on=True )
                #plt.title('Fastest lap speed by driver')
                plt.tight_layout()
                #plt.show()
                plt.savefig(f"{images_moto}/{cm}/{y}/{r}/{s}/plot_first_ten.jpg")
                plt.close()

                important_done.append('yes')
                new_dict = {'race': important_races, 
                            'is_done': important_done, 
                            'year': important_years, 
                            'class': important_classes}
                new_df = pd.DataFrame(new_dict)
                new_df.to_csv('/home/boris/Documents/matplotlib_exercize/done/qualifications_2.csv', index=False)