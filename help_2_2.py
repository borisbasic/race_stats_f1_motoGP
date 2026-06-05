import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
from sqlalchemy import create_engine, insert, Table, MetaData, select, and_, update
from datetime import datetime

def clear_speed(s):
    s1 = ''
    for i in range(len(s)):
        if s[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
            s1 = s1 + s[i]
    if s1 == '':
        return 0.0
    return float(s1)

engine = create_engine("mariadb+mariadbconnector://root:boris123@localhost:3306/motogp")
engine_n = create_engine(f"mariadb+mariadbconnector://motogpuser:3TEA8Tohoy6iwLbDVYEL@23.95.167.114:3306/motogp")
metadata = MetaData()

races_all = Table(
    'races',
    metadata,
    autoload_with=engine,
    autoload_replace=True
)

entries_all = Table(
    'entries',
    metadata,
    autoload_with=engine,
    autoload_replace=True
)

bikes = Table(
    'bikes',
    metadata,
    autoload_replace=True,
    autoload_with=engine
)

tyre_type = pd.read_csv('/home/boris/Documents/matplotlib_exercize/tyre_type/tyre_type_2025.csv')
for i, row in tyre_type.iterrows():
    select_row = select(entries_all).where(and_
                                           (entries_all.c.rider_name == row['driver_name'],
                                            entries_all.c.lap == row['lap'],
                                            entries_all.c.race_id == row['race'],
                                            entries_all.c.bike_class == 'motogp',
                                            entries_all.c.year == row['year'],
                                            entries_all.c.session == row['session']))
    with engine.connect() as conn:
        entry = conn.execute(select_row).fetchone()

        if entry is not None:
            if pd.isna(row['ft']):
                ft = 'n/a'
            else:
                ft = row['ft']
            if pd.isna(row['rt']):
                rt = 'n/a'
            else:                
                rt = row['rt']
            update_stmt = update(entries_all).where(entries_all.c.id == entry.id).values(ft=ft, rt=rt)
            conn.execute(update_stmt)
            conn.commit()
        
        print(i)
select_all_entries = select(entries_all)#.where(entries_all.c.bike_class=='moto3')

#with engine.connect() as conn:
#    all_entries_1 = conn.execute(select_all_entries).fetchall()



