import numpy as np
import matplotlib.pyplot as plt

years = [2014, 2015, 2016, 2017,
         2018, 2019, 2020, 2021]

income = [55, 56, 62, 61, 
          72, 73, 72, 75]

income_ticks = list(range(50, 81, 2))
print(income_ticks)
plt.plot(years, income)
plt.title('Income of John', fontsize=30, fontname='FreeSerif')
plt.xlabel('Year')
plt.ylabel('Income in USD')
plt.yticks(income_ticks, [f'${x}K' for x in income_ticks])
plt.legend()
plt.show()