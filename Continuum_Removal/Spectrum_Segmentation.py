from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def smooth_even(data):
    data_new = np.zeros((len(data), 2))
    # print(data)
    # print(data_new)
    data_new[0] = data[0]

    for i in range(0,len(data)-2):
        if i%2 == 0 :
            data_new[i + 1] = [data[i + 1, 0], (data[i, 1] + data[i + 2, 1]) / 2]
        else:
            data_new[i+1] = data[i+1]
    data_new[-2] = data[-2]
    data_new[-1] = data[-1]
    print(data)
    print(data_new)

    return data_new

def smooth_odd(data):
    data_new = np.zeros((len(data), 2))
    # print(data)
    # print(data_new)
    data_new[0] = data[0]

    for i in range(1,len(data)-2):
        if i%2 == 0 :
            data_new[i+1] = data[i+1]
        else:
            data_new[i + 1] = [data[i + 1, 0], (data[i, 1] + data[i + 2, 1]) / 2]

    data_new[-2] = data[-2]
    data_new[-1] = data[-1]
    print(data)
    print(data_new)

    return data_new


def segment(data, start, stop):
    start_index = np.where(data[:, 0] == start)[0][0]
    stop_index = np.where(data[:, 0] == stop)[0][0] + 1

    data = data[start_index:stop_index, :]
    valley_indices, _ = find_peaks(-data[:, 1])
    valleys = np.zeros((len(valley_indices), 2))

    j = 0

    for i in valley_indices:
        valleys[j, 0] = data[i, 0]
        valleys[j, 1] = data[i, 1]
        j += 1

    print(valleys)

    valleys = np.concatenate(([data[0, :]], valleys, [data[-1, :]]))
    plt.plot(valleys[:, 0], valleys[:, 1], 'r.')
    while len(valleys[:, 0]) > 9:
        # Finding valleys of valleys
        valley_indices, _ = find_peaks(-valleys[:, 1])
        valley_of_valleys = np.zeros((len(valley_indices), 2))
        j = 0

        for i in valley_indices:
            valley_of_valleys[j, 0] = valleys[i, 0]
            valley_of_valleys[j, 1] = valleys[i, 1]
            j += 1

        if len(valley_of_valleys) == 0:
            break
        valleys = valley_of_valleys

        valleys = np.concatenate(([data[0, :]], valleys, [data[-1, :]]))
        # plt.plot(valley_of_valleys[:, 0], valley_of_valleys[:, 1], 'ro')
        # cont = input('continut?(0/1)')
        print(valleys[:, 0])

    for point in valleys[:, 0]:
        plt.axvline(x=point, ymin=0.01, color='c')

    return valleys


raw_data = np.genfromtxt(
    'E:\Official_Project_Work\CUSAT\Misc\Rakhi Continuum Removal\FeAl 350-450.csv',
    delimiter=',', skip_header=0)

#raw_data = raw_data[0:10, :]

plt.axhline(y=0, color='k', linestyle='-')
plt.plot(raw_data[:, 0], raw_data[:, 1], 'r', label='Spectral Data')

# a = segment(raw_data, 221.01426, 666.97462)
# for i in range(5):
#     raw_data = smooth_even(raw_data)

#plt.plot(raw_data[:, 0], raw_data[:, 1], 'r')
#raw_data = smooth(raw_data)
plt.plot(raw_data[:, 0], raw_data[:, 1], 'g')

a = segment(raw_data, raw_data[0, 0], raw_data[-1, 0])

plt.show()
