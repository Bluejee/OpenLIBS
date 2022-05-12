from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

full_data = np.array([])
# Change number of files !!!!!
for i in range(4):
    fname = "E:\Official_Project_Work\CUSAT\Misc\Rakhi Continuum Removal\Continuum_Removed_" + str(i) + ".csv"
    raw_data = np.genfromtxt(fname, delimiter=',', skip_header=1)
    if full_data.size == 0:
        full_data = raw_data
    else:
        full_data = np.concatenate((full_data,raw_data))

print(full_data)
np.savetxt("E:\Official_Project_Work\CUSAT\Misc\Rakhi Continuum Removal\Continuum_Removed_total.csv", full_data, delimiter=",")

