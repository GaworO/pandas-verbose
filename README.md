
# pandas-verbose
*Adds a verbose variant to some important pandas features.*

## Description

*Important: This is built for pandas version 0.25.1. It may not work with other versions.*

The pandas library currently does not support a 'verbose' option for most of its DataFrame or Series methods except for `.info()`. This means that no printable output is generated when executing methods like `.drop()` or `.join()`, which in fact is a feature that many other languages provide by default. This gets more valuable when dealing with complex data preprocessing processes, involving multiple drop, select and join steps, an output like that would be useful for recognizing which step influenced the dataset in which way. Displaying the DataFrame / Series manually after each operation is ugly, 

This lightweight pandas extension aims to solve that problem by adding a decorator-like wrapper for some of the core DataFrame as well as Series methods. For that, the in-built pandas extension API is used to create a custom accessor, which allows easy to use access to the wrapped functions and eliminates the need to watch types (which is typically an issue encountered when simply adding a inheritance class of `pd.DataFrame` / `pd.Series`). 

## Usage

### DataFrames
Just use `df.verbose.someFunction()` instead of `df.someFunction()`. This supports the full list of arguments for the original function, including `inplace`. In case `inplace=False` is set, the returned object is of type `pd.DataFrame`.  Color coded output is supported by passing the additional optional argument `colored=True` (False is set by default).

*Supported methods:*

 - [x] `dropna()`
 - [ ] `drop()`
 - [ ] `join()`
 - [ ] `pd.createDummies()`

### Series
Just use `s.verbose.someFunction()` instead of `s.someFunction()`. This supports the full list of arguments for the original function, including `inplace`. In case `inplace=False` is set, the returned object is of type `pd.Series`.  Color coded output is supported by passing the additional optional argument `colored=True` (False is set by default).

*Supported methods:*

 - [ ] `dropna()`
 - [ ] `drop()`
