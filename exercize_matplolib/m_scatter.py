import numpy as np
import matplotlib.pyplot as plt

X_data = np.random.random(500) * 1000
y_data = np.random.random(500) * 1000

print(X_data)

plt.scatter(x=X_data, y=y_data, c='#aaa', marker='*', s=150, alpha=0.3)
                                #color                #size  #
plt.show()