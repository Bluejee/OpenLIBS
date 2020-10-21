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

    :return: The data collected from the user in a 2D array with columns of x and y.
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


def peak_analysis(raw_data, cut_off):
    """
    This function takes in the data and returns a list of x y values of the peaks.
    The find_peaks function in Scipy returns the indices of the peaks, we need the x and y values

    :param raw_data: The raw data obtained from the user(Spectrum)
    :param cut_off: The minimum intensity required for a peak to be selected
    :return: a list of x and y data of the peaks.
    """

    # Using the Y values to find the peaks
    # _ is to just ignore the other return values

    peak_indices, _ = find_peaks(raw_data[:, 1], height=cut_off)
    print('\nNumber of Peaks =', len(peak_indices))
    print('Peak Indices :: ')
    print(peak_indices)


    # Initialising the list of peaks using number of rows
    peak_list = np.zeros((len(peak_indices), 2))

    # Copying the X Y values based on calculated Indices.

    j = 0
    for i in peak_indices:
        peak_list[j, 0] = raw_data[i, 0]
        peak_list[j, 1] = raw_data[i, 1]
        j += 1

    print('\nPeak List :: ')
    print(peak_list,'\n\n')
    return peak_list


def element_comparison(peak_data, element_list, error_bar=0.1, match_threshold=3):
    """
    This function will look through a database of csv files, in which each file is named as element.csv where element
    will be the atomic symbol for the element it represents.
    Then it will compare the standard peaks of each element with the peaks in the data from the spectrum.
    The comparison will be made allowing an error in x. If the number of peaks that match are above a specific threshold
    the element will be added to a list.
    after comparing all elements given in the element_list the list of passed elements will be returned.
    The program will also return a list of peaks(Wavelengths) for the purpose of plotting.

    :param peak_data: The list of peaks in the given data.
    :param element_list: The list of elements to be checked from the database.
    :param error_bar: The error in wavelength within which a peak can be matched with the standard,
    set to 0.1nm as default.
    :param match_threshold: The number of peaks that has to match with the standard for the element to be present
    in the sample, set to 3 as default.
    :return: A list of elements that successfully passed the comparison and a list of matched peaks.
    """

    passed_elements = []
    matched_peaks = []
    # matched_peaks will have all the matched peaks of all elements

    # Running through all elements in the given list.
    for element in element_list:
        standard_data = np.genfromtxt('Element_Database\\' + element + '.csv', delimiter=',')
        standard_data_len = len(standard_data)
        peak_data_len = len(peak_data)
        num_matching_peaks = 0
        standard_peak_pos = 0
        peak_data_pos = 0

        print('Comparison starts for element', element, ':: ')  # testing to delete

        # While loop will run till one of the data set runs out.
        while standard_peak_pos < standard_data_len and peak_data_pos < peak_data_len:

            # Using \ to use 2 lines as line is too long
            # Using peak_data[peak_position,0] as we only compare the wavelength in column 1
            print('\n\n')  # testing to delete
            print('peak data position = ', peak_data_pos, 'standard data position = ',
                  standard_peak_pos)  # testing to delete
            print('peak data value = ', peak_data[peak_data_pos, 0], 'std data value = ',
                  standard_data[standard_peak_pos])  # testing to delete

            if peak_data[peak_data_pos, 0] > standard_data[standard_peak_pos] + error_bar:
                standard_peak_pos += 1
                print('Peak data is greater than standard data do increasing standard data.')  # testing to delete
            elif standard_data[standard_peak_pos] - error_bar <= peak_data[peak_data_pos, 0] <= \
                    standard_data[standard_peak_pos] + error_bar:
                # Using peak_data[peak_position] returns the x and y for plotting
                print(
                    'peak data in the region of error so increasing peak data and standard data.')  # testing to delete
                print('also increasing the number of matched peaks')  # testing to delete

                matched_peaks.append([peak_data[peak_data_pos, 0], peak_data[peak_data_pos, 1]])
                num_matching_peaks += 1
                peak_data_pos += 1
                standard_peak_pos += 1
                print('num_matched peaks = ', num_matching_peaks)  # testing to delete
            else:
                peak_data_pos += 1
                print('Peak data is less than the standard data so increasing the peak data')  # testing to delete

        # Checking if the element is present.
        if num_matching_peaks >= match_threshold:
            print('\nElement present')  # testing to delete
            passed_elements.append(element)
        print('\nComparison Ends for element', element, '. \n\n')  # testing to delete
    # Now the passed_elements list will have all the elements in the sample.
    return passed_elements, np.array(matched_peaks)


data = data_input()
peaks = peak_analysis(data, 5)
check_list = ['Cu', 'Al', 'Ca', 'Cr', 'Fe', 'K', 'Mg', 'Mn', 'Na', 'O', 'Si', 'Ti']
# check_list = ['O_Strong']
# check_list = ['Cu']
elements_present, match = element_comparison(peaks, check_list, error_bar=0.2)

# Test
print('Data :: ')
print(data)
print('Peaks :: ')
print(peaks)
print('Matched peaks :: ')
print(match)
print('Total number of Matched peaks = ', len(match))
print('Elements present :: ')
print(elements_present)
plt.plot(data[:, 0], data[:, 1], 'k-')
plt.plot(peaks[:, 0], peaks[:, 1], 'bo')

# plotting lines instead of points for matched peaks
plt.plot(match[:, 0], match[:, 1], 'go')

for point in match:
    plt.axvline(x=point[0], ymin=0.01, color='r')

# The code below is for the test when Oxygen is used.
# Not to be used for other elements

# Expected peaks in Oxygen
# oxygen = np.genfromtxt('Element_Database/O_Strong.csv', delimiter=',')
# oxygen_y = np.zeros(len(oxygen))
# oxygen_y = oxygen_y + 100000
# plt.plot(oxygen, oxygen_y, 'yo')


# The code below is for the test when copper is used.
# Not to be used for other elements

# Expected peaks in copper
# copper = np.genfromtxt('Element_Database/Cu.csv', delimiter=',')
# for point in copper:
#    plt.axvline(x=point, ymin=0.01, ymax=0.75)

# coppery = np.zeros(len(copper))
# coppery = coppery + 100000
# plt.plot(copper, coppery, 'yo')

# Detected peeks = Blue dots
# Expected peeks = yellow dots
# Matched peeks = green dots
# matched line = red


plt.show()
# End Test


print('Thank You')
