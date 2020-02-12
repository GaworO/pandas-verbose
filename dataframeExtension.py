### IMPORTS ###
import numpy as np
import pandas as pd

### CLASS EXTENSION ###
# Use the in-built pandas API to extend the DataFrame class with a new accessor. Syntax: df.verbose.someFunction() instead of df.someFunction()
@pd.api.extensions.register_dataframe_accessor("verbose")
class VerboseAccessor:

    # Constructor
    def __init__(self, pandas_obj):
        # Validation: Is the referenced object actually a DataFrame
        if not isinstance(pandas_obj, pd.DataFrame):
            raise AttributeError(
                "The verbose accessor can only be used with DataFrame objects. Use syntax df.verbose.dropna()")
        self._obj = pandas_obj

    # Static Color Codes for verbose output, used when the 'colored' flag is set in the below methods
    STYLE_RED = '\033[1;31m'
    STYLE_GREEN = '\033[0;32m'
    STYLE_END = '\033[0;0m'

    # Generates the string that is used as verbose output after each operation
    def generateVerboseString(self, functionName, _previousShape, _newShape, colored):
        # For usage in the verbose string
        self.dataType = "DataFrame"
        # Calculate the number of rows and columns that have been added / dropped.
        rowChange = _previousShape[0]-_newShape[0]
        columnChange = _previousShape[1]-_newShape[1]
        ## String concatenation
        print("\n{:20} {:7} {}{:^5d}{} rows and {:7} {}{:^5d}{} columns.\n".format(
            self.dataType + "." + functionName + '()',
            "dropped" if rowChange > 0 else "added",
            "" if rowChange == 0 or not colored else self.STYLE_RED if rowChange > 0 else self.STYLE_GREEN, # color codes
            rowChange,
            self.STYLE_END, # color reset
            "dropped" if columnChange > 0 else "added",
            "" if columnChange == 0 or not colored else self.STYLE_RED if columnChange > 0 else self.STYLE_GREEN, # color codes
            columnChange,
            self.STYLE_END # color reset
            )
        )

    # Extension of pandas' DataFrame.dropna() method. See pandas' docs for more information.
    def dropna(self, axis=0, how='any', thresh=None, subset=None, inplace=False, colored=False):
        # get unaltered shape before execution
        _previousShape = self._obj.shape
        # execute actual DataFrame method which is pd.DataFrame.dropna(...)
        res = self._obj.dropna(axis, how, thresh, subset, inplace)
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

    # Extension of pandas' DataFrame.drop() method. See pandas' docs for more information.
    def drop(self, labels=None, axis=0, index=None, columns=None, level=None, inplace=False, errors='raise', colored=False):
        # get unaltered shape before execution
        _previousShape = self._obj.shape
        # execute actual DataFrame method which is pd.DataFrame.drop(...)
        res = self._obj.drop(labels, axis, index, columns, level, inplace, errors)
        # Determine the new object to asses the count of changed rows / columns with, this varies according to the 'inplace' parameter
        # and thus makes the otherwise perfectly fit usage of (*args, **kwargs) impractical
        if inplace:
            _newShape = self._obj.shape
        else:
            _newShape = res.shape
        # print verbose output information about the executed function
        self.generateVerboseString("drop", _previousShape, _newShape, colored)
        # return result of original DataFrame.drop() method
        # this actually fixes a pandas usability issue where using df2 = df.someFunc(inplace=True) returns in df2 having NoneType
        if inplace:
            return self._obj
        else:
            return res


### TEST ###
df = pd.DataFrame(np.array([[1, 2, 3, np.nan], [4, 5, 6, np.nan], [
                  7, 8, 9, np.nan]]), columns=['a', 'b', 'c', 'd'])
df["e"] = np.nan
display(df.head())
df.verbose.drop(columns=["e", "a"], inplace=True, colored=True)
#print(type(df))
#df.verbose.drop(columns=["a", "b"], inplace=True)
print(df.head())
