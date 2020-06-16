"""

This program aims to take in a CSV file of a LIBS spectrum as an input. and then predict the elements present in the
sample from which the spectrum was taken.

The program flow can be described as :
1. Ask the user to give in the spectrum of the sample.
2. Run the spectrum through a peak analysing system in order to find the peaks.
3. compare the peaks with the existing NIST database in order to check the presence of each element.
4. If the criteria is satisfied  Return a list of elements present in the sample.

"""

from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt


def data_input():
    """
    This function asks the user for the location of the csv file to be processed,
    Creates a numpy array of the data and returns it.
    :return: data.
    """

    print('Hey there!, Welcome.')
    print('Kindly make sure that the file does not contain any headings.')
    print('Please enter the location(Path) of the CSV file containing the spectrum')

    location_data = input('Press Enter to use default path :: ')
    if location_data == '':
        location_data = 'Data.csv'
    else:
        pass

    return np.genfromtxt(location_data, delimiter=',')


data = data_input()

# Test
print(data)
plt.plot(data[:, 0], data[:, 1])
plt.show()
# End Test


print('Thank You')
