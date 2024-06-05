import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')
style.use('dark_background')

# links for styling
# https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html
# https://matplotlib.org/stable/tutorials/introductory/customizing/html

votes =  [10, 2, 5, 16, 22]
people = ['A', 'B', 'C', 'D', 'E']

plt.pie(x=votes, labels=people)
plt.legend(labels=people)
plt.show(

)