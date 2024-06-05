import numpy as np
import matplotlib.pyplot as plt

x = ['C++', 'C#', 'Pyhton', 'Java', 'Go']
y = [20, 50, 140, 1, 45]

plt.bar(x=x, height=y, color='#0a0', align='edge', edgecolor='red', lw=3)
plt.show()