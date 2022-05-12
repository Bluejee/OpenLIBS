"""

This Module contains functions which can be used to do the elemental analysis.
The actual command line program is different and is the complete true version for the process

"""

from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.optimize import curve_fit
import matplotlib.lines as mlines  # for creating the legends


# Functions
def data_input(location_data):
    """
    This function takes in the location of the csv file to be processed,
    Creates a numpy array of the data and returns it.

    :return: The data collected from the user in a 2D array with columns of x and y.
    """
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
    :return: a list of x and y data of the peaks, and the indexes of the position of the peaks in the raw data.
    """

    # Using the Y values to find the peaks
    # _ is to just ignore the other return values

    peak_indices, _ = find_peaks(raw_data[:, 1], height=cut_off)
    # print('\nNumber of Peaks =', len(peak_indices))
    # print('Peak Indices :: ')
    # print(peak_indices)

    # Initialising the list of peaks using number of rows
    peak_list = np.zeros((len(peak_indices), 2))

    # Copying the X Y values based on calculated Indices.

    j = 0
    for i in peak_indices:
        peak_list[j, 0] = raw_data[i, 0]
        peak_list[j, 1] = raw_data[i, 1]
        j += 1

    # print('\nPeak List :: ')
    # print(peak_list, '\n\n')
    return peak_list, peak_indices


def continuum_removal(raw_data):
    """
    This function takes in the raw data and then returns a new data which will have the continuum removed.
    The algorithm is to find the valley and then the valleys of the valleys to avoid jerky peaks, and then fit a
    9th order polynomial through it. This is then subtracted from the main data to get a continuum removed spectrum.

    :param raw_data:
    :return: A list of x and y values for the new data in the same format of the raw data.
    """

    def function(x, a0, a1, a2, a3, a4, a5, a6, a7, a8, a9):
        return a0 + a1 * x + a2 * (x ** 2) + a3 * (x ** 3) + a4 * (x ** 4) + a5 * (x ** 5) + a6 * (x ** 6) + a7 * (
                x ** 7) + a8 * (x ** 8) + a9 * (x ** 9)

    # Finding the valleys of the data
    peak_indices, _ = find_peaks(-raw_data[:, 1])
    valleys = np.zeros((len(peak_indices), 2))
    j = 0
    for i in peak_indices:
        valleys[j, 0] = raw_data[i, 0]
        valleys[j, 1] = raw_data[i, 1]
        j += 1

    # Finding valleys of valleys
    peak_indices, _ = find_peaks(-valleys[:, 1])
    valley_of_valleys = np.zeros((len(peak_indices), 2))
    j = 0
    for i in peak_indices:
        valley_of_valleys[j, 0] = valleys[i, 0]
        valley_of_valleys[j, 1] = valleys[i, 1]
        j += 1

    # Fitting the valleys of the valleys using a 9th order polynomial and finding its y value corresponding to the
    # x values of the data.

    popt, pcov = curve_fit(function, valley_of_valleys[:, 0], valley_of_valleys[:, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    y_continuum = function(raw_data[:, 0], *popt)

    # Subtracting the continuum from the spectrum.

    raw_data[:, 1] = raw_data[:, 1] - y_continuum

    # Setting the minimum value in the spectrum as 0 to correct the height of the spectrum
    min_int = min(raw_data[:, 1])

    for i in range(len(raw_data)):
        raw_data[i, 1] -= min_int

    return raw_data


def element_comparison(peak_data, element_list, lower_error_bar=-0.1, upper_error_bar=0.1, match_threshold=3):
    """
    This function will look through a database of csv files, in which each file is named as element.csv where element
    will be the atomic symbol for the element it represents.
    Then it will compare the standard peaks of each element with the peaks in the data from the spectrum.
    The comparison will be made allowing an error in x. If the number of peaks that match are above a specific threshold
    the element will be added to a list.
    after comparing all elements given in the element_list the list of passed elements will be returned.
    The program will also return a list of peaks(Wavelengths) for the purpose of plotting.

    When looking an a Spectrum, which is not ideal, the peaks would be shifted toward one direction and hence using an
    error system where symmetrical error is checked about the actual data would not work. hence we need a system which
    would allow us to set an interval of error within which the difference should lie so as to classify as a
    matched peak.


    :param peak_data: The list of peaks in the given data.
    :param element_list: The list of elements to be checked from the database.
    :param lower_error_bar: The minimum error in wavelength required for the peak to be a matching peak,
    set to -0.1 as default.
    :param upper_error_bar: The minimum error in wavelength required for the peak to be a matching peak,
    set to -0.1 as default
    :param match_threshold: The number of peaks that has to match with the standard for the element to be present
    in the sample, set to 3 as default.
    :return: A list of elements that successfully passed the comparison and a list of matched peaks.
    """

    passed_elements = []
    matched_peaks = []
    standard_matched_peaks = []
    # matched_peaks will have all the matched peaks of all elements

    # Opening the log file to print data into the file.
    element_comparison_log = open("Log_Files/Element_Comparison_Log.txt", "w")

    original_stdout = sys.stdout  # Save a reference to the original standard output
    sys.stdout = element_comparison_log  # Change the standard output to the file we created.

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

            if peak_data[peak_data_pos, 0] > standard_data[standard_peak_pos] + upper_error_bar:
                standard_peak_pos += 1
                print('Peak data is greater than standard data so increasing standard data.')  # testing to delete
            elif standard_data[standard_peak_pos] + lower_error_bar <= peak_data[peak_data_pos, 0] <= \
                    standard_data[standard_peak_pos] + upper_error_bar:
                # Using peak_data[peak_position] returns the x and y for plotting
                print(
                    'peak data in the region of error so increasing peak data and standard data.')  # testing to delete
                print('also increasing the number of matched peaks')  # testing to delete

                matched_peaks.append([peak_data[peak_data_pos, 0], peak_data[peak_data_pos, 1]])
                standard_matched_peaks.append(standard_data[standard_peak_pos])
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
        print('\n\n', num_matching_peaks, 'Peaks have matched for the element', element)
        print('Comparison Ends for element', element, '. \n\n')  # testing to delete
    # Now the passed_elements list will have all the elements in the sample.

    # Closing the log file.
    element_comparison_log.close()
    sys.stdout = original_stdout  # Reset the standard output to its original value
    return passed_elements, np.array(matched_peaks), np.array(standard_matched_peaks)
