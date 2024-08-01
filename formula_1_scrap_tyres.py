from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import matplotlib.pyplot as plt

op = webdriver.FirefoxOptions()
#op.add_argument("--headless")

driver = webdriver.Firefox(options=op)
link = 'https://www.motorsport.com/f1/results/2024/belgian-gp-639973/?st=TH'
race = 'BELGIA'
driver.get(link)
number_of_laps = 44
tyres = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ms-table_row')))
tyres_dict = {}
l = []
cond = False
for i in range(2, len(tyres)):
    ty = tyres[i].text.split('\n')
    j = 0
    for t in ty:
        
        if t == ':':
            l.append((ty[j-1], int(ty[j+1])))
        j = j + 1
    if ty[0].isnumeric():
        tyres_dict[ty[1]] = l
    else:
        tyres_dict[ty[0]] = l
    l = []
driver.close()
tyres_color = [('M', 'yellow'), ('H', 'white'), ('S', 'red'), ('W', 'blue'), ('I', 'green')]
i = 20
ylabels = []
yticks = [i for i in range(1, 21)]
xlabels = []
xticks = [i for i in range(1, number_of_laps + 1)]
plt.figure(figsize=(15,9), facecolor='#333333')
ax = plt.axes()
first = True
ax.set_facecolor("#333333")
num_of_laps = 1
for key, item in tyres_dict.items():
    ylabels.insert(0, key)
    for it in item:
        for tc in tyres_color:
            if tc[0] == it[0]:
                color = tc[1]
                break
        for it_ in range(num_of_laps, it[1] + num_of_laps):
            if first:
                plt.plot(it_, i, markersize=9, marker='o', markeredgecolor='#720e9e', markeredgewidth=3.3,color=color)
                first = False
            else:
                plt.plot(it_, i, markersize=9, marker='o',  color=color)
        first = True
        num_of_laps = num_of_laps + it[1]
    i = i - 1
    num_of_laps = 1
plt.yticks(ticks=yticks, labels=ylabels, fontweight='bold', fontname='Ubuntu',
                        fontsize=12,)
plt.xticks(ticks=xticks, labels=[f'{i}' for i in xticks], fontweight='bold', fontname='Ubuntu',
                        fontsize=10,)
plt.ylabel('Drivers', fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)
plt.xlabel('Laps', fontweight='bold', fontname='Ubuntu',
                        fontsize=15,)
plt.title('Compound usage', fontweight='bold', fontname='Ubuntu',
                        fontsize=17,)
plt.grid(color = '#696969', linestyle = '--', linewidth = 0.5)
plt.xlim(right=number_of_laps+0.5)
plt.tight_layout()
plt.savefig(f'/home/boris/Documents/matplotlib_exercize/{race}_2024_F1/coumpund_usage.jpg')
