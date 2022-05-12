from scipy.interpolate import CubicSpline
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import splev, splrep
import matplotlib.pyplot as plt
from scipy import stats



def lin(x,m,c):
    return m*x + c

data = np.genfromtxt('continum_removed.csv', delimiter=',')
x = data[:, 0]
y = data[:, 1]

print(x)
print(y)


z = np.linspace(x[0], x[-1], 1000)
print(z)



popt, pcov = curve_fit(lin, x, y, p0=[0,min(y)])

plt.plot(z, lin(z, *popt), 'b-')
plt.plot(x, y, 'r-')


y = y*(1/(y+ 0.000001))


print(y)


z = np.linspace(x[0], x[-1], 1000)



popt, pcov = curve_fit(lin, x, y, p0=[0,min(y)])

plt.plot(z, lin(z, *popt), 'g-')


plt.show()
