import numpy as np
import matplotlib.pyplot as plt

category_names = ['Strongly disagree', 'Disagree',
                  'Neither agree nor disagree', 'Agree', 'Strongly agree']
results = {
    'Question 1': [10, 15, 17, 32, 26],
    'Question 2': [26, 22, 29, 10, 13],
    'Question 3': [35, 37, 7, 2, 19],
    'Question 4': [32, 11, 9, 15, 33],
    'Question 5': [21, 29, 5, 5, 40],
    'Question 6': [8, 19, 5, 30, 38]
}
an = np.linspace(0, 2 * np.pi, 100)
labels = list(results.keys())
data = np.array(list(results.values()))
data_cum = data.cumsum(axis=1)
color = ['red', 'blue', 'green', 'black', 'yellow']
print(data[:, 0][0])

fig, ax = plt.subplots(figsize=(9,6))
ax.set_xlim(0, np.sum(data, axis=1).max())
xcenters = data_cum[:, 0] - data[:,0] + data[:, 0] / 2
print(xcenters)
ax.barh(labels, width=data[:, 0], left=data_cum[:, 0]-data[:, 0], label=labels[0], color=color[0])
for i in range(len(data[:, 0])):
    ax.text(xcenters[i], i, data[:, 0][i], ha='center', va='center', color='white')


ax.barh(labels, width=data[:, 1], left=data_cum[:, 1]-data[:, 1], label=labels[1], color=color[1])
xcenters = data_cum[:, 1] - data[:,1] + data[:, 1] / 2
for i in range(len(data[:, 1])):
    ax.text(xcenters[i], i, data[:, 1][i], ha='center', va='center', color='white')
ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')
plt.show()