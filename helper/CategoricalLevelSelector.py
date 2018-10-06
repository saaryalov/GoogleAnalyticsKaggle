import pandas as pd
import numpy as np

class CategoricalLevelSelection(object):
    '''
    This class is used to reduce the number of levels for categorical variables.


    Parameters
    ----------
    data : pd DataFrame
        DataFrame of one would like to make changes to

    key: string
        Unique ID to be ignored in study

    columns: List of strings(optinal)
        Column names to study, if not function finds categorical variabels automatically

    cols_to_drop: list of strings
        Names of additional columns to drop


    Notes
    -----
    None


    References
    -----
    For additional use cases refer to source analysis notebook


    See also
    --------

    '''

    def __init__(self):
        self.columns_to_change  = None
        self.key = None
        self.cols_to_ignore = None
        self.level_dictionary = None
        self.levels_to_keep = None
        self.verbose = None


    def __map_levels(self,df,column,change_to):
        series = df[column]
        levels = series.unique().tolist()
        levels_to_change = np.setdiff1d(levels,self.levels_to_keep[column]).tolist()
        series.replace(levels_to_change, change_to,inplace=True)
        return None

    def fit(self, data,thresh=0.05, columns=None, key=None, cols_to_ignore=None,verbose=False):
        '''
        Parameters
        ----------
        data : pd DataFrame
            DataFrame of one would like to use as basis for level selection

        key: string (Optional)
            Unique ID to be ignored in study

        columns: List of strings(optinal)
            Column names to study, if not function finds categorical variabels automatically

        cols_to_ignore: list of strings
            Names of additional columns to drop
        '''
        assert isinstance(data, pd.DataFrame)
        data = data.copy()
        #self.data = data.copy()

        # Drop Key
        self.key = key
        if key in data.columns:
            del data[key]

        # Create categorical data frame
        if columns is None:
            columns = list(data.select_dtypes(include="object").columns)

        # Drop cols to drop
        self.cols_to_ignore = cols_to_ignore
        if cols_to_ignore is not None:
            columns = np.setdiff1d(columns,cols_to_ignore)

        if key in columns:
            columns.remove(key)

        self.columns_to_change = columns

        # Compute
        temp_dictionary = {}
        levels_to_keep = {}
        for each in columns:
            if verbose:
                print(f"Working on {each}")
            counts = data[each].value_counts(dropna=False, normalize=True)
            temp_dictionary[each] = counts
            levels_to_keep[each] = list(counts[counts >= thresh].index)
        self.level_dictionary = temp_dictionary
        self.levels_to_keep = levels_to_keep
        #return copy.copy(self)
        return None

    def transform(self, new_data, change_to="Other", inplace=False, one_hot_encode=False,verbose=False):
        '''
        TODO: Work on series
        Parameters
        ----------
        new_data : pd.DataFrame, if a vector then pd.Series
            DataFrame one would like to make changes to

        thresh: numeric
            Minimum percentage of level space to keep a single level

        change_to: string - any of ("mode", "mode_ignore_missing",NA's, or any string you want to change it to)
            What to change dropped levels to

        inplace: bool (default False)
            If true performs changes at reference

        one_hot_encode: bool (default False)
            If transformation should do one hot encoding
            
    

        '''
        # Transform
        assert (isinstance(new_data, pd.DataFrame))
        
        self.verbose = verbose

        if not inplace:
            new_data = new_data.copy()

        for column in new_data.columns:
            if column in self.columns_to_change:
                if verbose:
                    print(f"changing {column}")
                self.__map_levels(new_data,column,change_to=change_to)

        if one_hot_encode:
            new_data = pd.get_dummies(new_data)

        return new_data

    def fit_transform(self, data, columns=None, key=None, cols_to_ignore=None,
                      thresh=0.1, change_to="Other", inplace=False, one_hot_encode=False):
        self.fit(data, columns, key, cols_to_ignore)
        df = self.transform(data, thresh, change_to, inplace, one_hot_encode)
        return  df

