import pdfplumber
import pandas as pd
import bar_chart_race as bcr
import matplotlib.pyplot as plt
num_of_races = 8
race = 'MONACO'
season = '2024'
pdf_path = f'/home/boris/Documents/matplotlib_exercize/{race}_{season}_F1/world_championship.pdf'

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


ws = pd.read_csv('/home/boris/Documents/matplotlib_exercize/formula_1_world_standings.csv', index_col=0)
ws = ws.cumsum()
print(ws)
bcr.bar_chart_race(
    #label_bars=False, 
    df=ws, 
    title=f'After {race}, World Standings 2024', 
    orientation='h', 
    sort='desc', 
    n_bars=10, 
    steps_per_period=40, 
    period_length=1500,
    filename=f'{race}_{season}_F1/world_standings.mp4', 
    cmap=drivers_colors,
    figsize=(15, 10),
    shared_fontdict={'family': 'Ubuntu', 'weight': 'bold',
                                    'color': 'rebeccapurple'},
    bar_kwargs={'alpha': .8},
    fixed_max=ws[ws.columns[0]].max()
)