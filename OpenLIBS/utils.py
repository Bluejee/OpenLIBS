"""
This module contains the classes that can be used to fetch libs spectra or to eork with analysed data.
"""
import os
import pandas as pd

class DataTable:
    """
    This is a class that can be used to further process analysed data output. Functions same as dictionary.
    
    Attributes
    ----------

    log: additional details/parameters provided in the analysis
    results: main data, contains matched peaks and standard peaks along with detected elements.
    """
    def __init__(self,data, *args, **kwargs):
        """ 
        Constructor for DataTable object
        
        Parameters
        ----------
        data: The output obtained from element_list_comparison as a dictionary object

        """
        
        self.log = data['log']
        self.results= data['result']



    def to_dataframe(self):
        """
        This function converts DataTable to a pandas dataframe
        
        Parameters
        -----------
        Requires no parameters. Only the DataTable object to be converted to the dataframe
        
        Returns
        -------
        A dictionary object containing keys which are detected elements with values of mathed peak and standard peaks in a pandas dataframe.
        """
        

        data = self.results
        key_list = data.keys()
        data_dict_sorted = dict()
        for key in key_list:
            data_dict_sorted[key] = dict()
            data_dict_sorted[key]['matched_peaks'] = []
            data_dict_sorted[key]['standard_peak'] = []
            data_dict_sorted[key]['ionization_state'] =[]
            data_dict_sorted[key]['intensity'] =[]
            if data[key]['is_match'] is True:
                for entry in data[key]["matched_peaks"]:
                    data_dict_sorted[key]['matched_peaks'].append(entry['Peak'])
                    data_dict_sorted[key]['standard_peak'].append(entry['Standard_Wavelength'])
                    data_dict_sorted[key]['ionization_state'].append(entry['Ionization_State'])
                    data_dict_sorted[key]['intensity'].append(entry['Intensity'])

        data_df = dict()

        for key in data_dict_sorted.keys():
            df = pd.DataFrame(data_dict_sorted[key])
            data_df[key] = df

        return data_df


    def ods_writer(self,path=None, split= True):

        """
        Writes the data to an ods file. Requires odspy package
        
        Parameters
        ----------

        path: path to the location where the ods file has to be generated and saved. The filename should be also included.
        eg: C:\\Users\\user\\desktop\\myfolder\\analysis.ods
        
        split: True or False as bool
          If two or more elements are matched, split = True will split individual element data into separate sheets in the same file.
          Split = False will generate a single sheet with an extra column.

        """
        

        data = self.to_dataframe()
        if split is True:
            with pd.ExcelWriter(path, engine='odf') as writer:
                for key in data.keys():
                    df = data[key]
                    df.to_excel(writer, sheet_name=key)
                    return
        with pd.ExcelWriter(path, engine='odf') as writer:
                for key in data.keys():
                    data[key]['Element'] = key

                df = pd.concat(data.values())
                df.to_excel(writer)
                return




class DataBase:

    """
    A class that can be used for database enquiry of standard spectral data

    Parameters
    ----------

    symbol: Symbol of the element whose information need to be fetched
    """

    def __init__(self, symbol):
        """
        Constructor for class DataBase. Creates a DataBase object for the element.
        
        Parameters
        ----------
        symbol: chemical symbol of the element whose dataset has to be fetched.

        """
        
        self.symbol = symbol
        self.file = os.path.join(os.path.dirname(__file__), 'Element_Database', f'{symbol}.csv')


    def get_data(self, line_type = None):
        """A method that returns the data set of the associated element
        
        Parameters
        ----------
        line_type: "P" or "S". P for persistent and S for strong. Defaults to None if not specified.
        
        Returns
        -------
        A pandas dataframe
        """
        

        if os.path.isfile(self.file):
            data = pd.read_csv(self.file)
            if line_type is None:
                return data
            return data['Line_type'==line_type]
        else:
            return f"The Database for {self.symbol} does not exist"

def get_data(symbol, line_type = None):
    """A method that returns the data set of the given element
        
    Parameters
    ----------
    symbol: The symbol of the element. Is case sensitive.
    line_type: "P" or "S". P for persistent and S for strong. Defaults to None if not specified.
        
    Returns
    -------
    A pandas dataframe
    """
        
    file = os.path.join(os.path.dirname(__file__), 'Element_Database', f'{symbol}.csv')
    if os.path.isfile(file):
        data = pd.read_csv(file)
        if line_type is None:
            return data
        return data['Line_type'==line_type]
    else:
        return f"The Database for {symbol} does not exist"