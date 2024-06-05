import numpy as np
import matplotlib.pyplot as plt

langs = ['Pyhton', 'C++', 'C#', 'Java', 'Go']
votes = [50, 24, 14, 6, 17]
explodes = [0.1, 0, 0, 0.05, 0]
plt.pie(x=votes, labels=langs, explode=explodes, autopct="%.2f%%", pctdistance=0.8, startangle=90)
plt.show()