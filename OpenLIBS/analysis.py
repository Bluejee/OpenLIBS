"""
This module contains the functions that are necessary to perform elemental analysis for a libs spectra.
"""
import pandas as pd


def detect_element(peak_data, element, line_type='P', lower_error=0.1, upper_error=0.1, match_threshold=3):
    """
    This function compares a list of peaks in a spectrum to the standard peaks for an element in a CSV file database.

    The CSV files are named after their corresponding elements, and the function checks the file corresponding to the
    required element.

    The CSV file contains 3 columns - Persistence, Wavelength, and Ionization_State.

    If only persistent peaks are to be checked then we only select those rows with the line_type being 'P'

    A peak is considered a match if its wavelength falls within a certain error range of the standard peak wavelength,
    determined by `lower_error` and `upper_error`. i.e. a peak is considered a match if,
    (standard_peak - lower_error) <= peak_value <= (standard_peak + upper_error)

    Here lower_error is also positive as it represents the magnitude of error allowed in the negative direction.
    A negative lower error would mean that the region to be checked is on the right side of the standard peak.

    When looking at a Spectrum, which is not ideal, the peaks would be shifted toward one direction and hence using an
    error system where symmetrical error is checked about the actual data would not work. Hence, we need a system which
    would allow us to set an interval of error within which the difference should lie for it to be a match.

    If the number of matched peaks for the element exceeds `match_threshold`, Then it is a successful match.

    Additionally, a list of all matched peaks(if any) and its details is returned.

    :param peak_data: A 2D array with the first column representing the wavelength (nm) and the second column
                      representing the intensity of peaks in the spectrum to be compared.
    :param element: The name (Atomic name) of the element to be compared.
    :param line_type: The type of standard line 'P' or 'S' to be checked. (P is a subset of S)
    :param lower_error: The difference in wavelength (nm) allowed to the left of the standard peak for a peak to be
                        considered a match.
    :param upper_error: The difference in wavelength (nm) allowed to the right of the standard peak for a peak to be
                        considered a match.
    :param match_threshold: The minimum number of peaks that must match the standard peaks for an element to be
                            considered a match.

    :return: A bool value of whether the element is a match, and a list of matching peaks, their intensities, and the
             standard peak they matched with.
    """

    # Load the element data from the CSV file
    element_file = f"Element_Database/{element}.csv"
    element_data = pd.read_csv(element_file)

    # Filter the data based on peak_type (P or S)
    if line_type == 'P':
        element_data = element_data[element_data['Line_type'] == 'P']

    # Initialize variables to store matched peaks and their details
    matched_peaks = []
    num_matches = 0

    # Iterate through each peak in peak_data
    for peak in peak_data:
        peak_value = peak[0]  # Wavelength is in the first column
        peak_intensity = peak[1]  # Intensity is in the second column

        # Check if any of the standard peaks match within the error range
        matches = element_data[
            (element_data['Wavelength'] - lower_error <= peak_value) &
            (element_data['Wavelength'] + upper_error >= peak_value)
            ]
        num_matches += len(matches)

        # Store the matched peaks and their details
        if not matches.empty:
            for _, peak_info in matches.iterrows():
                matched_peaks.append({
                    'Peak': peak_value,
                    'Intensity': peak_intensity,
                    'Standard_Wavelength': peak_info['Wavelength'],
                    'Ionization_State': peak_info['Ionisation_state']
                })

    # Check if the number of matched peaks exceeds the match_threshold
    is_match = num_matches >= match_threshold

    return is_match, matched_peaks


def element_list_comparison(peak_data, element_list, line_type='P', lower_error=0.1, upper_error=0.1,
                            match_threshold=3):
    """
    This is a function that performs comparison on a list of elements using the detect_element function.

    :param peak_data: A 2D array with the first column representing the wavelength (nm) and the second column
    representing the intensity of peaks in the spectrum to be compared.
    :param element_list: The list of element names (Atomic names) to be compared.
    :param line_type: The type of standard line 'P' or 'S' to be checked. (P is a subset of S)
    :param lower_error: The minimum difference in wavelength (nm) allowed for a peak to be considered a match.
    :param upper_error: The maximum difference in wavelength (nm) allowed for a peak to be considered a match.
    :param match_threshold: The minimum number of peaks that must match the standard peaks for an element to be
                            considered a match.
    :return:
        comparison_result: A dictionary containing information about the detected elements and their corresponding peaks.

        The output dictionary has the following structure:
        {
            "<Element_Symbol>": {
                "is_match": <bool>,
                "matched_peaks": [
                    {
                        "Peak": <float>,
                        "Intensity": <float>,
                        "Standard_Wavelength": <float>,
                        "Ionization_State": <int>
                    },
                    {
                        "Peak": <float>,
                        "Intensity": <float>,
                        "Standard_Wavelength": <float>,
                        "Ionization_State": <int>
                    },
                    ...
                ]
            },
            "<Element_Symbol>": {
                "is_match": <bool>,
                "matched_peaks": [
                    ...
                ]
            },
            ...
        }

        - <Element_Symbol>: The chemical symbol of the detected element, e.g., "Cu" for Copper, "Zn" for Zinc, etc.

        - "is_match": A boolean value (True or False) indicating whether the element is detected in the spectrum or not.
            - True: The element is present in the spectrum, and "matched_peaks" will contain information about the detected peaks.
            - False: The element is not present in the spectrum, and "matched_peaks" will be an empty list.

        - "matched_peaks": A list of dictionaries, where each dictionary represents a matched peak of the element in the spectrum.
            - "Peak": The observed peak value in the spectrum (measured in a unit specific to the spectroscopy).
            - "Intensity": The intensity or strength of the peak at the given wavelength.
            - "Standard_Wavelength": The standard wavelength value for the peak (measured in a consistent unit).
            - "Ionization_State": The ionization state of the element corresponding to the peak.
    """

    # Create a dictionary to store the results for each element
    comparison_results = {}
    detected_element_list = []
    # Iterate through each element in the element_list
    for element in element_list:
        # Perform comparison using the detect_element function
        is_match, matched_peaks = detect_element(peak_data, element, line_type, lower_error=lower_error,
                                                 upper_error=upper_error, match_threshold=match_threshold)
        if is_match:
            detected_element_list.append(element)
        # Store the results for the element in the comparison_results dictionary
        comparison_results[element] = {
            'is_match': is_match,
            'matched_peaks': matched_peaks
        }
    return comparison_results
