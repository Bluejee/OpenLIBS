from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def function(x, a0, a1, a2, a3, a4, a5, a6, a7, a8, a9):
    return a0 + a1 * x + a2 * (x ** 2) + a3 * (x ** 3) + a4 * (x ** 4) + a5 * (x ** 5) + a6 * (x ** 6) + a7 * (
            x ** 7) + a8 * (x ** 8) + a9 * (x ** 9)


def poly4(x, a0, a1, a2, a3, a4):
    # return a * np.exp(-((x - mean) ** 2) / (2 * (stddev ** 2)))
    return a0 + a1 * x + a2 * (x ** 2) + a3 * (x ** 3) + a4 * (x ** 4)

data = np.genfromtxt('E:\Official_Project_Work\CUSAT\Misc\Rakhi Continuum Removal\Cntd_removed_FeAl_350-450.csv', delimiter=',',skip_header=1)

l = len(data)

plt.axhline(y=0, color='k', linestyle='-')

plt.plot(data[:, 0], data[:, 1], 'r', label='Spectral Data')

#data[:, 1] = -data[:, 1]
peak_indices, _ = find_peaks(-data[:, 1])
#data[:, 1] = -data[:, 1]

valleys = np.zeros((len(peak_indices), 2))

j = 0

for i in peak_indices:
    valleys[j, 0] = data[i, 0]
    valleys[j, 1] = data[i, 1]
    j += 1

print(valleys)
plt.plot(valleys[:, 0], valleys[:, 1], 'b')

x = data[:, 0]
popt, pcov = curve_fit(function, valleys[:, 0], valleys[:, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
y = function(x, *popt)
plt.plot(x, y, 'y')

# Finding valleys of valleys

#valleys[:, 1] = -valleys[:, 1]
peak_indices, _ = find_peaks(-valleys[:, 1])
#valleys[:, 1] = -valleys[:, 1]

valley_of_valleys = np.zeros((len(peak_indices), 2))

j = 0

for i in peak_indices:
    valley_of_valleys[j, 0] = valleys[i, 0]
    valley_of_valleys[j, 1] = valleys[i, 1]
    j += 1

plt.plot(valley_of_valleys[:, 0], valley_of_valleys[:, 1], 'ro')

x = data[:, 0]
popt, pcov = curve_fit(function, valley_of_valleys[:, 0], valley_of_valleys[:, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
y = function(x, *popt)
plt.plot(x, y, 'g', label='Detected Continuum')


plt.title('Raw Spectrum', fontsize=30)
plt.xlabel('Wavelength (nm)', fontsize=30)
plt.ylabel('Intensity (a.u.)', fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=20)
plt.show()

data[:, 1] = data[:, 1] - y
print(data)
plt.axhline(y=0, color='k', linestyle='-')

min_int = min(data[:, 1])
#min_int = 0
for i in range(l):
    data[i, 1] -= min_int

#for i in range(l):
#    if data[i,1] <= 0:
#        data[i,1] = 0

plt.plot(data[:, 0], data[:, 1], 'r', label='Continuum Removed Spectrum')

np.savetxt("E:\Official_Project_Work\CUSAT\Misc\Rakhi Continuum Removal\Cntd_removed_2_FeAl_350-450.csv", data, delimiter=",")

plt.title('Continuum Removed Spectrum', fontsize=20)
plt.xlabel('Wavelength (nm)', fontsize=20)
plt.ylabel('Intensity (a.u.)', fontsize=20)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.legend(fontsize=15)
plt.show()
