import numpy as np
import pandas as pd

# Use the in-built pandas API to extend the DataFrame class with a new accessor. Syntax: df.verbose.someFunction() instead of df.someFunction()
@pd.api.extensions.register_dataframe_accessor("verbose")
class VerboseAccessor:
    
    # Constructor
    def __init__(self, pandas_obj):
        # Validation: Is the referenced object actually a DataFrame
        if not isinstance(pandas_obj, pd.DataFrame):
            raise AttributeError("The verbose accessor can only be used with DataFrame objects. Use syntax df.verbose.dropna()")
        self._obj = pandas_obj
        # For usage in the verbose string
        self.dataType = "DataFrame"
    
    # Generates the string that is used as verbose output after each operation
    def generateVerboseString(self, functionName, _previousShape):
        # Calculate the number of rows and columns that have been added / dropped.
        rowChange = _previousShape[0]-self._obj.shape[0]
        columnChange = _previousShape[1]-self._obj.shape[1]
        ## String concatenation
        print("{}.{}() {} {} rows and {} {} columns.".format(
            self.dataType,
            functionName,
            ("dropped" if rowChange > 0 else "added"),
            rowChange,
            ("dropped" if columnChange > 0 else "added"),
            columnChange
            )
        )
           
    # Extension of pandas' DataFrame.dropna() method. See pandas' docs for more information.
    def dropna(self, axis=0, how='any', thresh=None, subset=None, inplace=False):
        # get shape before execution
        _previousShape = self._obj.shape
        # execute actual function, inherited from pd.[].dropna(...)
        self._obj.dropna(axis, how, thresh,
                         subset, inplace)
        # print information about the executed function, mainly, which datatype the object had and if row / colum count changed.
        self.generateVerboseString("dropna", _previousShape)
       
        
    # Extension of pandas' DataFrame.drop() method. See pandas' docs for more information.
    def drop(self, labels=None, axis=0, index=None, columns=None, level=None, inplace=False, errors='raise'):
        # get shape before execution
        _previousShape = self._obj.shape
        # execute actual function, inherited from pd.[].dropna(...)
        self._obj.drop(labels, axis, index,
                       columns, level, inplace, errors)
        # print information about the executed function, mainly, which datatype the object had and if row / colum count changed.
        self.generateVerboseString("drop", _previousShape)


### TEST ###
df = pd.DataFrame(np.array([[1, 2, 3, np.nan], [4, 5, 6, np.nan], [7, 8, 9, np.nan]]), columns=['a', 'b', 'c', 'd'])
#print(df.head())
df.verbose.dropna(axis=1, inplace=True)
df.verbose.drop(columns=["a", "b"], inplace=True)
#print(df.head())
