---
execute:
  eval: false
jupyter: python3
title: Demo for objects and classes
toc-title: Table of contents
---

## Examples

Simple example with representer `__repr__`.

::: {.cell execution_count="1"}
``` {.python .cell-code}
import pandas as pd
import xarray as xr

class ArrayDataFrame(pd.DataFrame): # inherits pd.DataFrame class

    def set_array_column(self, arrays):
        self['arrays'] = arrays
        return self

    def __repr__(self):
        for_printing = self.copy()
        for_printing.arrays = [arr.min() for arr in self.arrays]
        return for_printing.__repr__()
```
:::

::: {.cell execution_count="2"}
``` {.python .cell-code}
ArrayDataFrame({'url': ['https://...']}).set_array_column([xr.DataArray()])
```
:::

Show example where class would help.

::: {.cell execution_count="3"}
``` {.python .cell-code}
import random
import numpy as np
import xarray as xr

def gen_data_array(size=10):
    data = (
        np.array([random.gauss(0,1) for _ in range(size**2)]).reshape(size, size))
    data = xr.DataArray(
        data = data,
        coords = {
            'x': [i * random.uniform(0,1) for i in range(size)],
            'y': [i * random.uniform(0,1) for i in range(size)]
        },
        dims=['x','y']
    )
    return data
```
:::

::: {.cell execution_count="4"}
``` {.python .cell-code}
gen_data_array(10)
```
:::

::: {.cell execution_count="5"}
``` {.python .cell-code}
df_len = 10
my_df = pd.DataFrame({
    'id': list(range(df_len)),
    'array': [gen_data_array(10) for _ in range(df_len)]
})
print(my_df)
```
:::

::: {.cell execution_count="6"}
``` {.python .cell-code}
class FunDataFrame(pd.DataFrame):
    # represent
    def __repr__(self):
        return 'stuff!'
```
:::

::: {.cell execution_count="7"}
``` {.python .cell-code}
my_df
```
:::

Add ipython method (under the hood concept)

::: {.cell execution_count="8"}
``` {.python .cell-code}
class FunDataFrame(pd.DataFrame):
    # represent
    def __repr__(self):
        return 'stuff!'
    # ipython method
    def _repr_html_(self):
        return 'more stuff!!!'
```
:::

::: {.cell execution_count="9"}
``` {.python .cell-code}
my_df
```
:::

::: {.cell execution_count="10"}
``` {.python .cell-code}
class FunDataFrame(pd.DataFrame):

    # attribute to make a dataframe
    @property
    def _df_for_repr_(self):
        df = self.drop(columns = ['array']).copy()
        return df
    # represent
    def __repr__(self):
        return self._df_for_repr_.__repr__()
    # ipython method
    def _repr_html_(self):
        return self._df_for_repr_._repr_html_()
```
:::

::: {.cell execution_count="11"}
``` {.python .cell-code}
my_df
```
:::

Set up my dataframe class to show what I want

::: {.cell execution_count="12"}
``` {.python .cell-code}
class FunDataFrame(pd.DataFrame):

    # define array_types (does not appear to be used yet) 
    array_types = [xr.DataArray]

    # attribute to return `array_cols`
    @property
    def array_cols(self):
        array_cols = []
        for col in self:
            if type(self[col][0]) == xr.DataArray:
                array_cols.append(col)
                return array_cols

    # more complicated attribute
    @property
    def _df_for_repr_(self):
        df = self.drop(columns = self.array_cols).copy()
        for array_col in self.array_cols:
            arr_str_list = []
            for arr in self[array_col]:
                arr_min = round(float(arr.x.min()), 2)
                arr_max = round(float(arr.x.max()), 2)
                arr_str_list.append(
                    f'DataArray(x ({arr_min}, {arr_max}))'
                )
            df[array_col] = arr_str_list
            #df[array_col] = ['DataArray' for _ in range(len(df))]
        return df
    
    # represent
    def __repr__(self):
        return self._df_for_repr_.__repr__()
    # ipython method
    def _repr_html_(self):
        return self._df_for_repr_._repr_html_()
```
:::

::: {.cell execution_count="13"}
``` {.python .cell-code}
my_df = FunDataFrame({
    'id': list(range(df_len)),
    'array': [gen_data_array(10) for _ in range(df_len)],
    'array2': [gen_data_array(10) for _ in range(df_len)]})
my_df
```
:::

## Demo

### Set up

::: {.cell execution_count="14"}
``` {.python .cell-code}
### load packages
import pandas as pd
import rioxarray as rxr
import xarray as xr
import geopandas as gpd
```
:::

What's the difference between a class and an object?

::: {.cell execution_count="15"}
``` {.python .cell-code}
### pandas dataframe class
help(pd.DataFrame)
```
:::

::: {.cell execution_count="16"}
``` {.python .cell-code}
### make a pandas df
my_df = pd.DataFrame({'column_1': list(range(10))})
my_df
```
:::

::: {.cell execution_count="17"}
``` {.python .cell-code}
### see what type of object it is
type(my_df)
```
:::

#### Dataframes

::: {.cell execution_count="18"}
``` {.python .cell-code}
### see what methods and attributes are available
dir(my_df)
```
:::

Classes can inherit from each other: dataframe --\> geodataframe

::: {.cell execution_count="19"}
``` {.python .cell-code}
### look at gdf
gpd.GeoDataFrame
```
:::

::: {.cell execution_count="20"}
``` {.python .cell-code}
### look at methods
my_df.mean()
type(my_df.mean())
```
:::

::: {.cell execution_count="21"}
``` {.python .cell-code}
## make dataframe more complicated
my_df.rename(columns = {'column_1': 'some_numbers'})
my_df
```
:::

#### Attributes

Attributes can be inconsistent. shape is an attribute:

::: {.cell execution_count="22"}
``` {.python .cell-code}
my_df.shape
```
:::

I might expect keys (looks at dictionary keys) to also be an attribute:

::: {.cell execution_count="23"}
``` {.python .cell-code}
### but it's a method instead
my_df.keys()
```
:::

SO it's confusing because we have methods that don't take arguments. And
the difference between a method that doesn't take arguments and an
attribute is just that an attribute doesn't take parentheses

We also have special attributes that we add to our objects but tha
aren't part of the class, like columns:

::: {.cell execution_count="24"}
``` {.python .cell-code}
### column_1 is an attribute of my dataframe, but not of the class dataframes
my_df.column_1
```
:::

::: {.cell execution_count="25"}
``` {.python .cell-code}
### this doesn't work!
# pd.DataFrame.column_1
```
:::

### Writing classes

Example: writing a class to store our latitude and longitude

::: {.cell execution_count="26"}
``` {.python .cell-code}
### bring in collections package for demo
import collections
```
:::

We can use the namedtuple method from collections as a lightweight way
to write our own class, but we can't customize it/add more methods:

::: {.cell execution_count="27"}
``` {.python .cell-code}
### we could call this a coordinate, then add a couple of fields
collections.namedtuple('Coordinate',
                       ['x', 'y'])

### and save this to coordinate
Coordinate= collections.namedtuple('Coordinate',
                                   ['x', 'y'])

### make an object of class Coordinate
my_coord = Coordinate(x = 5, y = 10)
my_coord
```
:::

::: {.cell execution_count="28"}
``` {.python .cell-code}
### can access it by name:
my_coord.x
```
:::

::: {.cell execution_count="29"}
``` {.python .cell-code}
### or by index:
my_coord[0]
```
:::

We can also write our own classes using the keyword "class". This lets
us define methods and attributes that will go with the class:

::: {.cell execution_count="30"}
``` {.python .cell-code}
class Coord():

    ### every class has methods listed indented in the class
    ### every class method must take the object that you're working with as the first argument (keyword for the argument is self)

    ### every class must have an init function
    def __init__(self, x, y):
        
        #### save x and y to store the attributes for the class
        self.x = x
        self.y = y
```
:::

::: {.cell execution_count="31"}
``` {.python .cell-code}
### make an object of that class
my_coord2 = Coord(5, 10)
my_coord2
```
:::

::: {.cell execution_count="32"}
``` {.python .cell-code}
### let's add a lat and lon and crs
class Coord():

    ### init function
    def __init__(self, x, y, crs = 'EPSG:4326'):
        
        #### save x and y to store the attributes for the class
        self.x = x
        self.y = y
        self.crs = crs


### make an object:
my_coord2 = Coord(5, 10)
my_coord2.x
```
:::

Then we can write methods for the class. For the demo, I'll show us
using a method that already exists:

::: {.cell execution_count="33"}
``` {.python .cell-code}
class Coord():

    ### init function
    def __init__(self, x, y, crs = 'EPSG:4326'):
        
        #### save x and y to store the attributes for the class
        self.x = x
        self.y = y
        self.crs = crs
    
    ### write repr method, using formatting string
    def __repr__(self):
        return f'Coord(x = {self.x}, y = {self.y})'
        
my_coord2 = Coord(5, 10)

### if i print it, it gives me the representation
print(my_coord2)
```
:::

::: {.cell execution_count="34"}
``` {.python .cell-code}
### add a method from geodataframe
class Coord():

    ### init function
    def __init__(self, x, y, crs = 'EPSG:4326'):
        
        #### save x and y to store the attributes for the class
        self.x = x
        self.y = y
        self.crs = crs
    
    ### write repr method, using formatting string
    def __repr__(self):
        return f'Coord(x = {self.x}, y = {self.y})'
    
    ### add method from gdf - add lat and lon as list
    def as_geoseries(self):
        return gpd.points_from_xy(x = [self.x], y = [self.y])
        
my_coord2 = Coord(5, 10)

# ### if i print it, it gives me the representation
# print(my_coord2)

my_coord2.as_geoseries()
```
:::

Now let's also define some properties of the class:

::: {.cell execution_count="35"}
``` {.python .cell-code}
### make class with defined properties
class Coord():

    ### init function
    def __init__(self, x, y, crs = 'EPSG:4326'):
        
        #### save x and y to store the attributes for the class
        self.x = x
        self.y = y
        self.crs = crs
    
    ### write repr method, using formatting string
    def __repr__(self):
        return f'Coord(x = {self.x}, y = {self.y})'
    
    ### add method from gdf - add lat and lon as list
    def as_geoseries(self):
        return gpd.points_from_xy(x = [self.x], y = [self.y])
    
    ### define lat 
    def lat(self):
        return self.y

    ### define longitude
    def lon(self):
        return self.x

### make coordiante object of class Coord        
my_coord2 = Coord(5, 10)
```
:::

::: {.cell execution_count="36"}
``` {.python .cell-code}
my_coord2.lat()
```
:::

::: {.cell execution_count="37"}
``` {.python .cell-code}
### make properties for our class using property decorator
class Coord():

    ### init function
    def __init__(self, x, y, crs = 'EPSG:4326'):
        
        #### save x and y to store the attributes for the class
        self.x = x
        self.y = y
        self.crs = crs
    
    ### write repr method, using formatting string
    def __repr__(self):
        return f'Coord(x = {self.x}, y = {self.y})'
    
    ### add method from gdf - add lat and lon as list
    def as_geoseries(self):
        return gpd.points_from_xy(x = [self.x], y = [self.y])
    
    ### define lat 
    @property
    def lat(self):
        return self.y

    ### define longitude
    @property
    def lon(self):
        return self.x

### make coordiante object of class Coord        
my_coord2 = Coord(5, 10)
```
:::

::: {.cell execution_count="38"}
``` {.python .cell-code}
# my_coord2.lat
my_coord2.lon
```
:::

::: {.cell execution_count="39"}
``` {.python .cell-code}
### add the ability to convert coordinates
class Coord():

    ### init function
    def __init__(self, x, y, crs = 'EPSG:4326'):

        ### save x, y, crs
        self.x = x
        self.y = y
        self.crs = crs

    ### repr method
    def __repr__(self):
        return f'Coord(x = {self.x}, y = {self.y})'
    
    ### add method from gdf
    def as_geoseries(self):
        return gpd.points_from_xy(x = [self.x], y = [self.y], crs = self.crs)
    
    ### define lat 
    @property
    def lat(self):
        return self.y

    ### define longitude
    @property
    def lon(self):
        return self.x
    

my_coord2 = Coord(5, 10)

my_coord2.as_geoseries().crs
```
:::

#### modify a pandas df to be able to put arrays in a column and not have it take forever to print

::: {.cell execution_count="40"}
``` {.python .cell-code}
### make a silly class that's just inheriting everything from another class without adding anything
class ArrayDataFrame(pd.DataFrame):
    pass

ArrayDataFrame()
```
:::

::: {.cell execution_count="41"}
``` {.python .cell-code}
### initialize it with some data
ArrayDataFrame({'url': ['https://...']})
```
:::

::: {.cell execution_count="42"}
``` {.python .cell-code}
### add a method called set_array_column
class ArrayDataFrame(pd.DataFrame):

    def set_array_column(self, arrays):

        ### define those arrays
        self['arrays'] = arrays
        return self
    
ArrayDataFrame({'url': ['https://...']}).set_array_column([xr.DataArray()])
```
:::

::: {.cell execution_count="43"}
``` {.python .cell-code}
xr.DataArray()
```
:::

::: {.cell execution_count="44"}
``` {.python .cell-code}
### add a representation method
class ArrayDataFrame(pd.DataFrame):

    def set_array_column(self, arrays):

        ### define those arrays
        self['arrays'] = arrays
        return self
    
    ### add representation method
    def __repr__(self):
        for_printing = self.copy()
        for_printing.arrays = [arr.min() for arr in self.arrays]
        return for_printing.__repr__()
    
ArrayDataFrame({'url': ['https://...']}).set_array_column([xr.DataArray()])
```
:::

#### Add some more packages for our demo

::: {.cell execution_count="45"}
``` {.python .cell-code}
import random
import numpy as np
```
:::

::: {.cell execution_count="46"}
``` {.python .cell-code}
### function to generate random values and puts them in xarray data array, lets us control the size
def gen_data_array(size = 10):
    data = (
        np.array([random.gauss(0, 1) for _ in range(size**2)])
        .reshape(size, size))
    da = xr.DataArray(
        data = data,
        coords = {
            'x': [i * random.uniform(0, 1) for i in range(size)],
            'y': [i * random.uniform(0, 1) for i in range(size)]}
    )
    return da

### define dataframe length
df_len = 10

### make dataframe
my_df = pd.DataFrame({
    'id': list(range(df_len)),
    'array': [gen_data_array(10) for _ in range(df_len)]})

my_df
```
:::

If we make the array bigger, it will really slow down! So let's make a
class that won't be so slow at dealing with and printing arrays:

::: {.cell execution_count="47"}
``` {.python .cell-code}
### make a dataframe
my_df = pd.DataFrame({
    'id': list(range(df_len)),
    'array': [gen_data_array(100) for _ in range(df_len)]})

my_df
```
:::

::: {.cell execution_count="48"}
``` {.python .cell-code}
### make the class
class FunDataFrame(pd.DataFrame):

    ### represent
    def __repr__(self):

        ### have it print 'stuff'
        return 'stuff!'
    

### define df length
df_len = 10

### make a dataframe
my_df = FunDataFrame({
    'id': list(range(df_len)),
    'array': [gen_data_array(10) for _ in range(df_len)]})

print(my_df)
```
:::

::: {.cell execution_count="49"}
``` {.python .cell-code}
### same class, but add representation method from ipython
class FunDataFrame(pd.DataFrame):

    ### represent
    def __repr__(self):

        ### have it print 'stuff'
        return 'stuff!'
    
    ### ipython method
    def _repr_html_(self):
        return 'more stuff!!!!'
    

### define df length
df_len = 10

### make a dataframe
my_df = FunDataFrame({
    'id': list(range(df_len)),
    'array': [gen_data_array(10) for _ in range(df_len)]})

my_df
```
:::

::: {.cell execution_count="50"}
``` {.python .cell-code}
### add a property
class FunDataFrame(pd.DataFrame):

    ### write a function to make a dataframe
    @property
    def _df_for_repr_(self):

        ### drop the array column
        df = self.drop(columns = ['array']).copy()

        ### return it as a dataframe
        return df

    ### represent
    def __repr__(self):
        return self._df_for_repr_.__repr__()
    
    ### ipython method
    def _repr_html_(self):
        return self._df_for_repr_._repr_html_()
    

### define df length
df_len = 10

### make a dataframe
my_df = FunDataFrame({
    'id': list(range(df_len)),
    'array': [gen_data_array(100) for _ in range(df_len)]})

my_df
```
:::

::: {.cell execution_count="51"}
``` {.python .cell-code}
### we've dropped the array column
### now we can play around with the representation methods
### but we still want to do something with the array column!
class FunDataFrame(pd.DataFrame):

    ### make array as a property
    @property
    def array_cols(self):

        ### define an empty list
        array_cols = []

        ### iterate the columns
        for col in self:

            ### check object type
            if type(self[col][0]) == xr.DataArray:
                    
                    ### append to my array cols
                    array_cols.append(col)

                    ### return the array cols
                    return array_cols
                                       
    
    ### write a function to make a dataframe
    @property
    def _df_for_repr_(self):

        ### drop the array column
        df = self.drop(columns = ['array']).copy()

        ### return it as a dataframe
        return df

    ### represent
    def __repr__(self):
        return self._df_for_repr_.__repr__()
    
    ### ipython method
    def _repr_html_(self):
        return self._df_for_repr_._repr_html_()
    

### define df length
df_len = 10

### make a dataframe
my_df = FunDataFrame({
    'id': list(range(df_len)),
    'array': [gen_data_array(100) for _ in range(df_len)]})

my_df
```
:::

::: {.cell execution_count="52"}
``` {.python .cell-code}
my_df.array_cols
```
:::

::: {.cell execution_count="53"}
``` {.python .cell-code}
### let's add another property 
class FunDataFrame(pd.DataFrame):

    ### tell it what I define as an array
    array_types = [xr.DataArray]

    ### make array as a property
    @property
    def array_cols(self):

        ### define an empty list
        array_cols = []

        ### iterate the columns
        for col in self:

            ### check object type
            if type(self[col][0]) in self.array_types:
                    
                    ### append to my array cols
                    array_cols.append(col)

                    ### return the array cols
                    return array_cols
                                       
    
    ### write a function to make a dataframe
    @property
    def _df_for_repr_(self):

        ### drop the array column
        df = self.drop(columns = ['array']).copy()

        ### return it as a dataframe
        return df

    ### represent
    def __repr__(self):
        return self._df_for_repr_.__repr__()
    
    ### ipython method
    def _repr_html_(self):
        return self._df_for_repr_._repr_html_()
    

### define df length
df_len = 10

### make a dataframe
my_df = FunDataFrame({
    'id': list(range(df_len)),
    'array': [gen_data_array(100) for _ in range(df_len)]})

my_df
```
:::

::: {.cell execution_count="54"}
``` {.python .cell-code}
### let's define what we consider to be an array
class FunDataFrame(pd.DataFrame):

    ### tell it what I define as an array
    array_types = [xr.DataArray]

    ### make array as a property
    @property
    def array_cols(self):

        ### define an empty list
        array_cols = []

        ### iterate the columns
        for col in self:

            ### check object type
            if type(self[col][0]) in self.array_types:
                    
                    ### append to my array cols
                    array_cols.append(col)

                    ### return the array cols
                    return array_cols
                                       
    
    ### write a function to make a dataframe
    @property
    def _df_for_repr_(self):

        ### drop the array column
        df = self.drop(columns = self.array_cols).copy()

        ### deal with the array columns
        for array_col in self.array_cols:
             
             ### replace array column with somethng that tells me its a dataarray
             df[array_col] = ['DataArray' for _ in range(len(df))]

        ### return it as a dataframe
        return df

    ### represent
    def __repr__(self):
        return self._df_for_repr_.__repr__()
    
    ### ipython method
    def _repr_html_(self):
        return self._df_for_repr_._repr_html_()
    

### define df length
df_len = 10

### make a dataframe
my_df = FunDataFrame({
    'id': list(range(df_len)),
    'array': [gen_data_array(10) for _ in range(df_len)]})

my_df
```
:::

::: {.cell execution_count="55"}
``` {.python .cell-code}
### now let's add something to display something for the array column so it doesn't look empty
class DataFrame(pd.DataFrame):

    ### tell it what an array is
    array_types = [xr.DataArray]

    ### make array as a property
    @property
    def array_cols(self):
        array_cols = []
        for col in self:
            if type(self[col][0]) in self.array_types:
                array_cols.append(col)
        return array_cols
    
    ### and then don't need to change anything in the next property becuase the property decorator turns it into an attribute

    @property
    def _df_for_repr_(self):
        df = self.drop(columns = self.array_cols).copy()

        ### we dropped the arrays in the new df we made
        for array_col in self.array_cols:

            ### replace array column with something to tell me it's a dataarray
            df[array_col] = ['DataArray' for _ in range(len(df))]
        return df

    def __repr__(self):
        return self._df_for_repr_.__repr__()
    
    def _repr_html_(self):
        return self._df_for_repr_._repr_html_()

### define dataframe length
df_len = 10

### make dataframe
my_df = DataFrame({
    'id': list(range(df_len)),
    'array': [gen_data_array(100) for _ in range(df_len)],
    'array2': [gen_data_array(100) for _ in range(df_len)]})
my_df
```
:::

::: {.cell execution_count="56"}
``` {.python .cell-code}
### let's loop through the array columns and pull out some info on each array
class DataFrame(pd.DataFrame):

    ### tell it what an array is
    array_types = [xr.DataArray]

    ### make array as a property
    @property
    def array_cols(self):
        array_cols = []
        for col in self:
            if type(self[col][0]) in self.array_types:
                array_cols.append(col)
        return array_cols
    
    ### and then don't need to change anything in the next property becuase the property decorator turns it into an attribute

    @property
    def _df_for_repr_(self):
        df = self.drop(columns = self.array_cols).copy()
        for array_col in self.array_cols:

            ### make array string list to fill
            arr_str_list = []

            ### iterate through each row to compute for each array
            for arr in self[array_col]:

                ### gonna assume the arrays are a certain way to get structure of code, then can generalize later on
                ### assume we have an x coordinate
                ### use format string
                ### let's round the numbers so they don't have a ton of decimal points
                arr_str_list.append(
                    f'DataArray(x ({round(float(arr.x.min()), 2)}))')

            ### add it
            df[array_col] = arr_str_list
        return df

    def __repr__(self):
        return self._df_for_repr_.__repr__()
    
    def _repr_html_(self):
        return self._df_for_repr_._repr_html_()

### define dataframe length
df_len = 10

### make dataframe
my_df = DataFrame({
    'id': list(range(df_len)),
    'array': [gen_data_array(100) for _ in range(df_len)],
    'array2': [gen_data_array(100) for _ in range(df_len)]})
my_df
```
:::

::: {.cell execution_count="57"}
``` {.python .cell-code}
### let's add the max value as well
class DataFrame(pd.DataFrame):

    ### tell it what an array is
    array_types = [xr.DataArray]

    ### make array as a property
    @property
    def array_cols(self):
        array_cols = []
        for col in self:
            if type(self[col][0]) in self.array_types:
                array_cols.append(col)
        return array_cols
    

    @property
    def _df_for_repr_(self):
        df = self.drop(columns = self.array_cols).copy()
        for array_col in self.array_cols:
            arr_str_list = []
            for arr in self[array_col]:

                ## ADD here as variables
                arr_min = round(float(arr.x.min()), 2)
                arr_max = round(float(arr.x.max()), 2)
                arr_str_list.append(
                    f'DataArray(x ({arr_min}, {arr_max}))')

            ### add it
            df[array_col] = arr_str_list
        return df

    def __repr__(self):
        return self._df_for_repr_.__repr__()
    
    def _repr_html_(self):
        return self._df_for_repr_._repr_html_()

### define dataframe length
df_len = 10

### make dataframe
my_df = DataFrame({
    'id': list(range(df_len)),
    'array': [gen_data_array(100) for _ in range(df_len)],
    'array2': [gen_data_array(100) for _ in range(df_len)]})
my_df
```
:::
