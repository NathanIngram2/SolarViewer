import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 31)
y = np.sin(x)


plt.plot(x, y, 'o-', color='lightgrey', label='sin')

plt.legend()
plt.title('Test Plot')
plt.show()
