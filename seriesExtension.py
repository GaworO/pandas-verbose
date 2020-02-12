### IMPORTS ###
import numpy as np
import pandas as pd

### CLASS EXTENSION ###
# Use the in-built pandas API to extend the Series class with a new accessor. Syntax: s.verbose.someFunction() instead of s.someFunction()
@pd.api.extensions.register_series_accessor("verbose")
class VerboseAccessor:

    # Constructor
    def __init__(self, pandas_obj):
        # Validation: Is the referenced object actually a Series
        if not isinstance(pandas_obj, pd.Series):
            raise AttributeError(
                "The verbose accessor can only be used with Series objects. Use syntax s.verbose.dropna()")
        self._obj = pandas_obj

    # Static Color Codes for verbose output, used when the 'colored' flag is set in the below methods
    STYLE_RED = '\033[1;31m'
    STYLE_GREEN = '\033[0;32m'
    STYLE_END = '\033[0;0m'

    # Generates the string that is used as verbose output after each operation
    def generateVerboseString(self, functionName, _previousShape, _newShape, colored):
        # For usage in the verbose string
        self.dataType = "Series"
        # Calculate the number of rows and columns that have been added / dropped.
        rowChange = _newShape[0]-_previousShape[0]
        ## String concatenation
        print("{:20} {:7} {}{:^5d}{} rows.".format(
            self.dataType + "." + functionName + '()',
            "dropped" if rowChange < 0 else "added",
            "" if rowChange == 0 or not colored else self.STYLE_RED if rowChange < 0 else self.STYLE_GREEN, # color codes
            abs(rowChange),
            self.STYLE_END, # color reset
            )
        )

    # Extension of pandas' Series.dropna() method. See pandas' docs for more information.
    def dropna(self, axis=0, inplace=False, how=None, colored=False):
        # get unaltered shape before execution
        _previousShape = self._obj.shape
        # execute actual Series method which is pd.Series.dropna(...)
        res = self._obj.dropna(axis=axis, inplace=inplace, how=how)
        # Determine the new object to asses the count of changed rows / columns with, this varies according to the 'inplace' parameter
        # and thus makes the otherwise perfectly fit usage of (*args, **kwargs) impractical
        if inplace:
            _newShape = self._obj.shape
        else:
            _newShape = res.shape
        # print verbose output information about the executed function
        self.generateVerboseString("dropna", _previousShape, _newShape, colored)
        # return result of original DataFrame.dropna() method
        # this actually fixes a pandas usability issue where using df2 = df.someFunc(inplace=True) returns in df2 having NoneType
        if inplace:
            return self._obj
        else:
            return res



### TEST ###
s = pd.Series(np.array([1, 2, 3, np.nan]))
display(s.head())

s.verbose.dropna(inplace=False, how=None, colored=True)
display(s.head())
