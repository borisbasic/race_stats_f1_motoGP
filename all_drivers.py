import pandas as pd
import os

class_moto = os.listdir('/home/boris/Documents/matplotlib_exercize/moto_pdfs')
all_riders_teams = pd.DataFrame()
for cm in class_moto:
    if cm not in ['motogp', 'moto2', 'moto3']:
        continue
    year = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}')
    for y in year:
        if not os.path.isdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}'):
            continue
        races = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}') 
        for r in races:
            seasion = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}')
            for s in seasion:
                #try:
                try:
                    drivers = pd.read_csv(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/entry.csv')
                except:
                    continue
                drivers = drivers[['team']]
                drivers['year'] = y
                drivers['class'] = cm
                all_riders_teams = pd.concat([all_riders_teams, drivers])
                all_riders_teams = all_riders_teams.drop_duplicates(keep='first')
                print(all_riders_teams)

#all_riders_teams = all_riders_teams.drop_duplicates(inplace=True)
print(all_riders_teams)
all_riders_teams.to_csv(f'all_drivers.csv', index=False)