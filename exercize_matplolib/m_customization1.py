import numpy as np
import matplotlib.pyplot as plt

stock_a = [100, 102, 99, 101, 101, 100, 102]
stock_b = [90, 95, 102, 104, 105, 103, 109]
stock_c = [110, 115, 100, 100, 98, 95, 105]

plt.plot(stock_a, label='Company1')
plt.plot(stock_b, label='Company2')
plt.plot(stock_c, label='Company3') # x se automatski popunjava ako nije zadat na osnovu duzine 
plt.legend(loc='lower center')
plt.show()