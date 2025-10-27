import pandas as pd
import io
def to_real_time(t):
    new_time = str(t)
    minutes = int(new_time.split('.')[0])//60
    seconds = int(new_time.split('.')[0])%60
    miliseconds = int(new_time.split('.')[1])
    if seconds < 10:
        seconds = f'0{seconds}'
    if miliseconds < 10:
        miliseconds = f'00{miliseconds}'
    elif miliseconds < 100:
        miliseconds = f'0{miliseconds}'
    return f'{minutes}:{seconds}.{miliseconds}'
j = 122.234
print(to_real_time(j))

# Kreiran mapping funkcija za hex boje timova
def get_team_hex_color(team_name, year, class_name):
    team_clean = team_name.strip()
    
    # MotoGP timovi - glavne boje
    if "Ducati" in team_clean:
        return "#DC143C"  # Crvena
    elif "Yamaha" in team_clean or "Monster" in team_clean:
        return "#0066CC"  # Plava
    elif "LCR" in team_clean:
        return "#8B8684"  # Narandžasta
    elif "Honda" in team_clean or "Repsol" in team_clean:
        return "#FF4500"  # Narandžasta
    elif  "GASGAS" in team_clean or "Tech3" in team_clean or "Tech 3" in team_clean:
        return "#B8500A"  # KTM narandžasta
    elif "KTM" in team_clean or "Red Bull KTM" in team_clean:
        return "#FF6600"  # KTM narandžasta
    elif "Aprilia" in team_clean:
        return "#A41DA8"  # Zelena
    elif "Suzuki" in team_clean:
        return "#0080FF"  # Svetlo plava
    elif "Pramac" in team_clean:
        return "#F700FF"  # Žuta
    elif "Gresini" in team_clean:
        return "#4169E1"  # Kraljevsko plava
    elif "VR46" in team_clean:
        return "#95A003"  # Fluorozelena žuta
    elif "Trackhouse" in team_clean:
        return "#2278B2"  # Amerikanska crvena
    
    # Moto2/Moto3 specifični timovi
    elif "Leopard" in team_clean:
        return "#228B8B"  # Zelena
    elif "Aspar" in team_clean or "CFMOTO" in team_clean:
        return "#DC143C"  # Crvena
    elif "CIP" in team_clean or "Green Power" in team_clean:
        return "#047504"  # Zelena
    elif "Marc VDS" in team_clean or "EG 0,0" in team_clean:
        return "#FFD700"  # Žuta
    elif "Speed Up" in team_clean or "SpeedUp" in team_clean:
        return "#DC143C"  # Crvena
    elif "American Racing" in team_clean:
        return "#B22222"  # Amerikanska crvena
    elif "Intact GP" in team_clean or "Liqui Moly" in team_clean:
        return "#D1002DB9"  # Tirkizna
    elif "Fantic" in team_clean:
        return "#FF69B4"  # Ružičasta
    elif "MT Helmets" in team_clean or "MSI" in team_clean:
        return "#000000"  # Crna
    elif "Snipers" in team_clean or "Rivacold" in team_clean:
        return "#4682B4"  # Čelično plava
    elif "BOE" in team_clean:
        return "#125A12"  # Lime zelena
    elif "SIC58" in team_clean:
        return "#FF1493"  # Deep pink
    elif "Honda Team Asia" in team_clean:
        return "#FF4500"  # Honda narandžasta
    elif "Petronas" in team_clean:
        return "#0059FF"  # Spring zelena
    elif "Mahindra" in team_clean:
        return "#8B0000"  # Tamno crvena
    elif "Estrella Galicia" in team_clean:
        return "#FFD700"  # Žuta
    elif "Avintia" in team_clean:
        return "#2F4F4F"  # Tamno siva
    elif "Forward" in team_clean:
        return "#4169E1"  # Kraljevsko plava
    elif "Italtrans" in team_clean:
        return "#074907"  # Zelena (italijanska)
    elif "SAG Team" in team_clean or "Mandalika" in team_clean:
        return "#FF8C00"  # Tamno narandžasta
    elif "Kiefer Racing" in team_clean:
        return "#800080"  # Ljubičasta
    elif "AGR Team" in team_clean:
        return "#DC143C"  # Crvena
    elif "RW Racing" in team_clean:
        return "#4169E1"  # Kraljevsko plava
    elif "Pons" in team_clean:
        return "#FF1493"  # Deep pink
    elif "Garage Plus" in team_clean or "Interwetten" in team_clean:
        return "#FF8C00"  # Tamno narandžasta
    elif "Federal Oil" in team_clean:
        return "#000080"  # Navy plava
    elif "Dynavolt" in team_clean:
        return "#0A7072"  # Tirkizna
    elif "NTS" in team_clean:
        return "#8A2BE2"  # Blue violet
    elif "MV Agusta" in team_clean:
        return "#B22222"  # Firebrick crvena
    elif "Blusens" in team_clean:
        return "#4B0082"  # Indigo
    elif "Paul Bird" in team_clean:
        return "#696969"  # Dim gray
    elif "Attack Performance" in team_clean:
        return "#FF4500"  # Orange red
    elif "Cardion AB" in team_clean:
        return "#008B8B"  # Dark cyan
    elif "IodaRacing" in team_clean:
        return "#9932CC"  # Dark orchid
    elif "NGM" in team_clean:
        return "#1A5232"  # Sea green
    elif "Power Electronics" in team_clean:
        return "#DC143C"  # Crimson
    
    # Default boje po klasama
    if class_name == "motogp":
        return "#FF0000"  # Crvena za MotoGP
    elif class_name == "moto2":
        return "#0000FF"  # Plava za Moto2
    elif class_name == "moto3":
        return "#192594"  # Zelena za Moto3
    else:
        return "#5F2C187D"  # Siva kao fallback
    

def stript_columns(row):
    return row['team'].strip()    
import pandas as pd

all_drivers_df = pd.read_csv('all_drivers.csv')
all_drivers_df['team'] = all_drivers_df.apply(stript_columns, axis=1)
all_drivers_df['hex_color'] = all_drivers_df.apply(lambda x: get_team_hex_color(x['team'], x['year'], x['class']), axis=1)

all_drivers_df = all_drivers_df.drop_duplicates(keep='first').reset_index(drop=True)
all_drivers_df.to_csv('all_drivers_with_colors.csv', index=False)