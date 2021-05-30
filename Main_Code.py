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
import sys
from scipy.optimize import curve_fit
import matplotlib.lines as mlines  # for creating the legends


# By default the print function outputs to the console screen, to make it print to a file, we can change its path.
# We initially save the current output stream to a variable, change the out to the file we want, and then in the end,
# change it back to the actual output stream.

# Functions
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


# Work in Progress.
def wavelength_avg_half_maximum(peak_indices, raw_data):
    """
    This function will use the list of peaks, its indices and the raw data, to calculate the wavelength average, at half
    the maximum intensity. This will take the intensity of the peak as the maximum, and then find the closest point to
    the half intensity value. The point can lie above or below the half intensity value, but should be minimum in error.

    :param peak_indices: The indices of the peaks in the raw data.
    :param raw_data: The raw spectrum to be used in analysis.

    :return: a list of x and y data of the peaks where x is the wavelength average at half max intensity and y is the
    original intensity of the peak.
    """

    # This has caused some errors as can be seen from the scratch Trial_Tests.py
    # Hence fot now we are discarding the work.
    # This can be taken up after we find a way to interpolate the line between the points or
    # fit it with an equally spaced curve.
    # as this will work best with equally spaced y values.

    new_peak_list = []
    for i in peak_indices:

        half_peak_int = raw_data[i, 1] / 2

        # Finding the left point at half maximum intensity.
        j = i
        error = half_peak_int
        while True:  # This will keep working till we find the point with least error
            least_error_left = raw_data[j, 0]  # wavelength of least error on left
            j = j - 1
            if error < abs(raw_data[j, 1] - half_peak_int):  # if the initial error is smaller that's the point we want.
                break
            else:  # if the initial error is larger we set the new one as the error and repeat
                error = abs(raw_data[j, 1] - half_peak_int)
        print('Point of least error left =', least_error_left)

        # Finding the right point at half maximum intensity.
        j = i
        error = half_peak_int
        while True:  # This will keep working till we find the point with least error
            least_error_right = raw_data[j, 0]  # wavelength of least error on left
            j = j + 1
            if error < abs(raw_data[j, 1] - half_peak_int):  # if the initial error is smaller that's the point we want.
                break
            else:  # if the initial error is larger we set the new one as the error and repeat
                error = abs(raw_data[j, 1] - half_peak_int)
        print('Point of least error right =', least_error_right)
        wavelength_average = (least_error_left + least_error_right) / 2
        print('wavelength_avg =', wavelength_average)
        peak_at_index = [wavelength_average, raw_data[i, 1]]
        new_peak_list.append(peak_at_index)
    return new_peak_list


# Work in Progress.
def peak_function_fit(peak_data, raw_data):
    """
    This function is still a thought in progress,
        1. the function starts from the raw data, the first point, and then collects all points till the end of the
        first peak, then fits it using a gaussian or lagrangian fit. then repeats this process to completely and
        individually fit all peaks.
        2. The function uses the list of all peaks and the raw data to fit each peak and return the list of peaks and
        corresponding intensities.

    :param peak_data: The list of peaks and corresponding intensities.
    :param raw_data: The raw spectrum to be used in analysis.
    :return:
    """


# Work in Progress.
def manual_helper(peak_data, element_list, lower_limit_error, upper_limit_error, error_bar=0.1):
    # Opening the log file to print data into the file.
    manual_helper_log = open("Log_Files/Manual_Comparison_Log.txt", "w")
    original_stdout = sys.stdout  # Save a reference to the original standard output
    sys.stdout = manual_helper_log  # Change the standard output to the file we created.
    print("Error Bar :: ", error_bar)
    print()
    print(" Std_Peak |   Error  |  Element ")
    print("--------------------------------")
    for peak in peak_data:
        print("   Matched Peak :: %8.4f   " % (peak[0]))
        for element in element_list:
            standard_data = np.genfromtxt('Element_Database\\' + element + '.csv', delimiter=',')

            for std_peak in standard_data:
                if std_peak - error_bar <= peak[0] <= std_peak + error_bar:
                    if lower_limit_error < (peak[0] - std_peak) < upper_limit_error:
                        print(" %8.4f |  %6.3f  |" % (std_peak, peak[0] - std_peak), element)
        print('\n')
    # Closing the log file.
    manual_helper_log.close()
    sys.stdout = original_stdout  # Reset the standard output to its original value


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


# Check lists for common applications.

check_list_persistent = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl',
                         'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As',
                         'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In',
                         'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb',
                         'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl',
                         'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk',
                         'Cf', 'Es']

check_list_strong = ['H_Strong', 'He_Strong', 'Li_Strong', 'Be_Strong', 'B_Strong', 'C_Strong', 'N_Strong', 'O_Strong',
                     'F_Strong', 'Ne_Strong', 'Na_Strong', 'Mg_Strong', 'Al_Strong', 'Si_Strong', 'P_Strong',
                     'S_Strong', 'Cl_Strong', 'Ar_Strong', 'K_Strong', 'Ca_Strong', 'Sc_Strong', 'Ti_Strong',
                     'V_Strong', 'Cr_Strong', 'Mn_Strong', 'Fe_Strong', 'Co_Strong', 'Ni_Strong', 'Cu_Strong',
                     'Zn_Strong', 'Ga_Strong', 'Ge_Strong', 'As_Strong', 'Se_Strong', 'Br_Strong', 'Kr_Strong',
                     'Rb_Strong', 'Sr_Strong', 'Y_Strong', 'Zr_Strong', 'Nb_Strong', 'Mo_Strong', 'Tc_Strong',
                     'Ru_Strong', 'Rh_Strong', 'Pd_Strong', 'Ag_Strong', 'Cd_Strong', 'In_Strong', 'Sn_Strong',
                     'Sb_Strong', 'Te_Strong', 'I_Strong', 'Xe_Strong', 'Cs_Strong', 'Ba_Strong', 'La_Strong',
                     'Ce_Strong', 'Pr_Strong', 'Nd_Strong', 'Pm_Strong', 'Sm_Strong', 'Eu_Strong', 'Gd_Strong',
                     'Tb_Strong', 'Dy_Strong', 'Ho_Strong', 'Er_Strong', 'Tm_Strong', 'Yb_Strong', 'Lu_Strong',
                     'Hf_Strong', 'Ta_Strong', 'W_Strong', 'Re_Strong', 'Os_Strong', 'Ir_Strong', 'Pt_Strong',
                     'Au_Strong', 'Hg_Strong', 'Tl_Strong', 'Pb_Strong', 'Bi_Strong', 'Po_Strong', 'At_Strong',
                     'Rn_Strong', 'Fr_Strong', 'Ra_Strong', 'Ac_Strong', 'Th_Strong', 'Pa_Strong', 'U_Strong',
                     'Np_Strong', 'Pu_Strong', 'Am_Strong', 'Cm_Strong', 'Bk_Strong', 'Cf_Strong', 'Es_Strong']

check_list_nobel_gas = ['He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn']

check_list_bronze_p = ['Cu', 'Sn']

check_list_brass_p = ['Cu', 'Zn']

check_list_bronze_s = ['Cu_Strong', 'Sn_Strong']

check_list_brass_s = ['Cu_Strong', 'Zn_Strong']

check_list_empty = ['']

check_list_custom = ['Fe', 'Mg', 'Si', 'Na', 'Ca', 'Ti', 'S', 'O']
check_list_steel = ['Fe', 'Cr', 'Ni', 'Mn', 'Si', 'C', 'P', 'S', 'N']
check_list_input = [input("Enter Element to be checked :: ")]

# Input and Analysis

data = data_input()
set_cutoff = 140  # Using a variable to store the minimum intensity cutoff.

plt.plot(data[:, 0], data[:, 1], 'r')
# data = continuum_removal(data)
plt.plot(data[:, 0], data[:, 1], 'g')
plt.plot(data[[0, -1], 0], [set_cutoff, set_cutoff], 'k')  # to view cutoff
plt.show()

peaks, indices = peak_analysis(data, set_cutoff)

manual_helper(peaks, check_list_custom, lower_limit_error=-0.3, upper_limit_error=0.3, error_bar=0.25)
# manual_helper(peaks, check_list_persistent, error_bar=0.1)

# for default use, the lower and upper error bar will have the same magnitude of the value, but the lower
# one would be negative.
elements_present, match_data, match_std = element_comparison(peaks, check_list_custom, lower_error_bar=0.2,
                                                             upper_error_bar=0.6, match_threshold=3)

# Expected peaks in any element
plot_choice = input('Do you want to display the lines of any one element along with the plot(y/n) :: ')
if plot_choice in ['y', 'Y']:
    plot_element = input('Enter the element do you want to display :: ')
    element_lines = np.genfromtxt('Element_Database/' + plot_element + '.csv', delimiter=',')
    for point in element_lines:
        check_lines = plt.axvline(x=point, ymin=0.01, ymax=0.75, label=('Standard Lines of ' + plot_element))

# Results
original_stdout = sys.stdout  # Save a reference to the original standard output

# Data
log = open("Log_Files/Data_Log.txt", "w")
sys.stdout = log  # Change the standard output to the file we created.
print('Data :: ')
np.set_printoptions(threshold=sys.maxsize)  # For not truncating the Data.
print(data)
log.close()

# Peaks
log = open("Log_Files/Peak_List_Log.txt", "w")
sys.stdout = log  # Change the standard output to the file we created.
print('Peaks :: ')
print(peaks)
log.close()

# Match Data
log = open("Log_Files/Matched_Peak_Log.txt", "w")
sys.stdout = log  # Change the standard output to the file we created.
print('Matched peaks :: ', len(match_data))
print(match_data)
print('\n\nStandard Peaks :: ')
print(match_std)
log.close()

sys.stdout = original_stdout

print('\n\nElements present :: ', len(elements_present))
print(elements_present)

spectral_plot, = plt.plot(data[:, 0], data[:, 1], 'k-',
                          label='Spectral Data')  # , has been used to discard the second return from the plot function
detected_peaks_plot, = plt.plot(peaks[:, 0], peaks[:, 1], 'bo', label='Detected peaks')

matched_peak_plot, = plt.plot(match_data[:, 0], match_data[:, 1], 'go', label='Matched Peaks')

# plotting lines instead of points for matched peaks
# for point in match_data:
#     plt.axvline(x=point[0], ymin=0.01, color='r')


# plotting standard matches to view difference

for point in match_std:
    plt.axvline(x=point, ymin=0.01, color='y')

# Plot details

plt.title('Optical Emission Spectrum', fontsize=30)
plt.xlabel('Wavelength (nm)', fontsize=30)
plt.ylabel('Intensity (a.u.)', fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
yellow_line_plot = mlines.Line2D([], [], color='yellow', label='Standard Lines From Database')
# Creating an Empty legend to show detected elements.
empty_legend_plot = mlines.Line2D([], [], color='none', label=('Elements Present = ' + str(elements_present)))

# Legends with element list and check_lines
# plt.legend(handles=[spectral_plot, detected_peaks_plot, matched_peak_plot, yellow_line_plot, check_lines,
# empty_legend_plot], fontsize=20)

# Legends without element list and check_lines
plt.legend(handles=[spectral_plot, detected_peaks_plot, matched_peak_plot, yellow_line_plot],
           fontsize=20)

plt.show()
# End Test

print('Thank You')
