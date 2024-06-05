import numpy as np
import matplotlib.pyplot as plt

ax = plt.axes(projection='3d')

x = np.arange(-5, 5, 0.1)
y = np.arange(-5, 5, 0.1)
print(x)

X, Y = np.meshgrid(x, y)
print(X)
print(Y)
Z = np.sin(X) * np.cos(Y)

ax.plot_surface(X, Y, Z, cmap='Spectral')
ax.set_title('3D Plot')

plt.show()
