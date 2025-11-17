import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import matplotlib.image as mpimg
from matplotlib.patches import FancyBboxPatch
sns.set_theme()
plt.style.use('ggplot')
background = '/home/boris/Downloads/b3b9110aa41ab877323a5041802d3f4e.jpg'
from sqlalchemy import create_engine, insert, Table, MetaData, select, and_
engine = create_engine("mariadb+mariadbconnector://root:boris123@localhost:3306/motogp")
metadata = MetaData()
races_all = Table(
    'races',
    metadata,
    autoload_with=engine,
    autoload_replace=True
)
fastest_lap_all = Table(
    'fastest_laps',
    metadata,
    autoload_with=engine,
    autoload_replace=True
)
class_moto = os.listdir('/home/boris/Documents/matplotlib_exercize/moto_pdfs')
def equal_time(row):
    time = row['sector_1'] + row['sector_2'] + row['sector_3'] + row['sector_4']
    if time - row['time'] < 0.001 and time - row['time'] > -0.001:
        return 'yes'
    else:
        return 'no'
images_moto = '/home/boris/Documents/motogp_api/images'

for cm in class_moto:
    important_things_csv = '/home/boris/Documents/matplotlib_exercize/done/fastest_lap.csv'
    important_things_csv = pd.read_csv(important_things_csv)
    important_races = important_things_csv['race'].tolist()
    important_years = important_things_csv['year'].tolist()
    important_classes = important_things_csv['class'].tolist()
    important_done = important_things_csv['is_done'].tolist()
    important_session = important_things_csv['session'].tolist()
    if cm not in ['motogp', 'moto2', 'moto3']:
        continue
    year = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}')
    for y in year:
        #if y not in ['2025']:
        #    continue
        list_of_year = os.listdir(f'{images_moto}/{cm}')
        if y not in list_of_year:
            os.mkdir(f'{images_moto}/{cm}/{y}')
        if not os.path.isdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}'):
            continue
        races = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}') 
        for r in races:
            list_of_races = os.listdir(f'{images_moto}/{cm}/{y}')
            if r not in list_of_races:
                os.mkdir(f'{images_moto}/{cm}/{y}/{r}')
            seasion = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}')
            for s in seasion:
                dones = important_things_csv[(important_things_csv['race'] == r) & (important_things_csv['year'] == int(y)) & (important_things_csv['class'] == cm) & (important_things_csv['session'] == s)]['is_done'].tolist()
            
                if 'yes' in dones:
                    continue
                list_of_seasion = os.listdir(f'{images_moto}/{cm}/{y}/{r}')
                if s not in list_of_seasion:
                    os.mkdir(f'{images_moto}/{cm}/{y}/{r}/{s}')

                if not os.path.exists(f"/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/Analysis.pdf"):
                        continue
                drivers = f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/entry.csv'
                bikes = '/home/boris/Documents/matplotlib_exercize/all_drivers_with_colors.csv'
                try:
                    drivers = pd.read_csv(drivers)
                except:
                    continue
                bikes = pd.read_csv(bikes)
                drivers_ = []
                drivers_colors = []
                drivers_numbers = []
                dri = []
                dr_c = []
                dri_n = []
                year_ = int(y)
                for i, row in drivers.iterrows():
                    if row['rider_surname'] == 'RUEDA Jose':
                        rueda = row['rider_surname'].split(' ')[1] + ' ' + row['rider_name'] + ' ' + row['rider_surname'].split(' ')[0]
                        drivers_.append(rueda)
                    else:
                        drivers_.append(f'{row["rider_name"]} {row["rider_surname"]}')
                    drivers_numbers.append(f'{row["number"]}')
                    try:
                        driver_team = row['team'].strip()
                        color = bikes[(bikes['team']==driver_team) & (bikes['year']==year_)]['hex_color'].values[0]
                    except:
                        color = '#808080'
                    drivers_colors.append(color)
                fs_1 = 0
                fs_1_driver = ''
                fs_2 = 0
                fs_2_driver = ''
                fs_3 = 0
                fs_3_driver = ''
                fs_4 = 0
                fs_4_driver = ''
                for d in drivers_:
                    try:
                        help = pd.read_csv(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/{d}_analysis.csv')
                        
                        help['yes'] = help.apply(equal_time, axis=1)
                        help = help[help['yes'] == 'yes']
                    except:
                        continue
                    
                    if len(help) == 0:
                        continue
                    if fs_1 == 0:
                        fs_1 = help[help['sector_1'] > 0]['sector_1'].min()
                        fs_1_driver = d
                        fs_2 = help[help['sector_2'] > 0]['sector_2'].min()
                        fs_2_driver = d
                        fs_3 = help[help['sector_3'] > 0]['sector_3'].min()
                        fs_3_driver = d
                        fs_4 = help[help['sector_4'] > 0]['sector_4'].min()
                        fs_4_driver = d

                        continue
                    
                    fs_1_help = help[help['sector_1'] > 0]['sector_1'].min()
                    fs_2_help = help[help['sector_2'] > 0]['sector_2'].min()
                    fs_3_help = help[help['sector_3'] > 0]['sector_3'].min()
                    fs_4_help = help[help['sector_4'] > 0]['sector_4'].min()
                    if fs_1_help < fs_1:
                        fs_1 = fs_1_help
                        fs_1_driver = d
                    if fs_2_help < fs_2:
                        fs_2 = fs_2_help
                        fs_2_driver = d
                    if fs_3_help < fs_3:
                        fs_3 = fs_3_help
                        fs_3_driver = d     
                    if fs_4_help < fs_4:
                        fs_4 = fs_4_help
                        fs_4_driver = d
                lap_time = fs_1 + fs_2 + fs_3 + fs_4
                lap_time = round(lap_time, 3)
                fastets_lap_dict = {
                    'lap_time': lap_time,
                    'sector_1': fs_1,
                    'sector_1_driver': fs_1_driver,
                    'sector_2': fs_2,
                    'sector_2_driver': fs_2_driver,
                    'sector_3': fs_3,
                    'sector_3_driver': fs_3_driver,
                    'sector_4': fs_4,
                    'sector_4_driver': fs_4_driver
                }
                print(fs_1, fs_2, fs_3, fs_4, lap_time)
                #if any(x==pd.nan for x in )
                fastest_lap_df = pd.DataFrame([fastets_lap_dict])
                fastest_lap_df.to_csv(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/fastest_lap.csv', index=False)
                select_race = select(races_all).where(and_(races_all.c.race==r,
                                                                races_all.c.year==int(y),))
                with engine.connect() as conn:
                    race_result = conn.execute(select_race).fetchone()
                    race_id = race_result.id
                insert_stmt = insert(fastest_lap_all).values(
                    sector_1=fs_1,
                    sector_1_racer=fs_1_driver,
                    sector_2=fs_2,  
                    sector_2_racer=fs_2_driver,
                    sector_3=fs_3,
                    sector_3_racer=fs_3_driver,
                    sector_4=fs_4,
                    sector_4_racer=fs_4_driver,
                    total_time=lap_time,
                    race_id=race_id,
                    session=s,
                    bike_class=cm
                )
                with engine.connect() as conn:
                    result = conn.execute(insert_stmt)
                    conn.commit()


                fig, ax = plt.subplots(figsize=(15, 9))  
                ax.set_xlim(0, lap_time+0.5)
                ax.set_ylim(0, 5)
                
                color_1 = drivers_colors[drivers_.index(fs_1_driver)]
                color_2 = drivers_colors[drivers_.index(fs_2_driver)]
                color_3 = drivers_colors[drivers_.index(fs_3_driver)]
                color_4 = drivers_colors[drivers_.index(fs_4_driver)]
                rect_s1 = FancyBboxPatch(
                    (0.5, 2), fs_1-0.5, 1,
                    boxstyle="round,pad=0.2,rounding_size=0.15",  # zaobljenje ivica
                    linewidth=0.5,
                    edgecolor="none",
                    facecolor=color_1,
                    alpha=0.8,
                    mutation_aspect=1,
                    zorder=2,
                    #shadow=True,  
                )
                rect_s2 = FancyBboxPatch(
                    (fs_1+0.5, 2), fs_2-0.5, 1,
                    boxstyle="round,pad=0.2,rounding_size=0.15",  # zaobljenje ivica
                    linewidth=0.5,
                    edgecolor="none",
                    facecolor=color_2,
                    alpha=0.8,
                    mutation_aspect=1,
                    zorder=2,
                    #shadow=True,  
                )
                rect_s3 = FancyBboxPatch(
                    (0.5+fs_1 + fs_2, 2), fs_3-0.5, 1,
                    boxstyle="round,pad=0.2,rounding_size=0.15",  # zaobljenje ivica
                    linewidth=0.5,
                    edgecolor="none",   
                    facecolor=color_3,
                    alpha=0.8,
                    mutation_aspect=1,
                    zorder=2,
                    #shadow=True,  
                )
                rect_s4 = FancyBboxPatch(
                    (0.5+fs_1 + fs_2 + fs_3, 2), fs_4-0.5, 1,
                    boxstyle="round,pad=0.2,rounding_size=0.15",  # zaobljenje ivica
                    linewidth=0.5,      
                    edgecolor="none",
                    facecolor=color_4,  
                    alpha=0.8,
                    mutation_aspect=1,
                    zorder=2,   
                    #shadow=True,  
                )

                ax.add_patch(rect_s1)
                ax.add_patch(rect_s2)
                ax.add_patch(rect_s3)
                ax.add_patch(rect_s4) 
                ax.axis('off')
                bg = mpimg.imread(background)
                plt.imshow(bg, extent=[-0.5, lap_time+0.5, -0.5, 5.5], aspect='auto', alpha=0.3)
                plt.text(lap_time/2, 3.5, f'Fastest Lap: {lap_time} seconds', fontweight='bold', fontsize=20, color="black", va='center', ha='center', clip_on=True )
                plt.text(lap_time/2, 1, f'Race: {r} {y} \nSession: {s} \n{cm.upper()}', fontweight='bold', fontsize=20, color="black", ha='center', va='center',clip_on=True )
                plt.text(fs_1 / 2, 2.5, f'Sector 1 \n {fs_1} s\n{fs_1_driver}', fontweight='bold', color='white', fontsize=12, ha='center', va='center')
                plt.text(fs_1 + fs_2 / 2, 2.5, f'Sector 2\n {fs_2} s\n{fs_2_driver}',fontweight='bold', color='white', fontsize=12, ha='center', va='center')  
                plt.text(fs_1 + fs_2 + fs_3 / 2, 2.5, f'Sector 3\n {fs_3} s\n{fs_3_driver}',fontweight='bold', color='white', fontsize=12, ha='center', va='center')
                plt.text(fs_1 + fs_2 + fs_3 + fs_4 / 2, 2.5, f'Sector 4\n {fs_4} s\n{fs_4_driver}',fontweight='bold', color='white', fontsize=12, ha='center', va='center')
                plt.tight_layout()
                plt.savefig(f"{images_moto}/{cm}/{y}/{r}/{s}/fastest_lap.jpg")
                #plt.show()
                plt.close()
                important_done.append('yes')
                important_session.append(s)
                important_races.append(r)
                important_years.append(y)
                important_classes.append(cm)
                new_dict = {'race': important_races, 
                            'is_done': important_done, 
                            'year': important_years, 
                            'class': important_classes,
                            'session': important_session}
                new_df = pd.DataFrame(new_dict)
                new_df.to_csv('/home/boris/Documents/matplotlib_exercize/done/fastest_lap.csv', index=False)