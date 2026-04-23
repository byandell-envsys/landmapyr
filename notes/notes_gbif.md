---
execute:
  eval: false
jupyter: python3
title: "Habitat suitability under climate change: Step 1"
toc-title: Table of contents
---

Demo going through parts of Step 1 of the latest coding assignment.
Katherine Siegel, 25 Feb 2025.

-   [Recording](https://canvas.colorado.edu/courses/115453/modules/items/6278820)
-   [Protected Areas Database
    (PAD-US)](https://www.usgs.gov/programs/gap-analysis-project/science/pad-us-data-download)
-   [Brian Notes](#brian-notes)
-   [Katherine Notes](#katherine-notes)

## Brian Notes

::: {.cell execution_count="1"}
``` {.python .cell-code}
pip install pygbif
```
:::

::: {.cell execution_count="2"}
``` {.python .cell-code}
## reproducible file paths
import os
from glob import glob
import pathlib

## GBIF packages
import pygbif.occurrences as occ
import pygbif.species as species
from getpass import getpass

## unzip and handle gbif data
import zipfile
import time

## spatial data
import geopandas as gpd
import xrspatial as xr

## other data
import numpy as np
import pandas as pd
import rioxarray as rxr
import rioxarray.merge as rxrm

## invalid geometries
from shapely.geometry import MultiPolygon, Polygon

## viz data
import holoviews as hv
import hvplot.pandas
import hvplot.xarray
```
:::

::: {.cell execution_count="3"}
``` {.python .cell-code}
# make repro file paths
data_dir = os.path.join(
    # home directory
    pathlib.Path.home(),
    
    ### eda directory
    'earth-analytics',
    'data',
    'hab_suit'
)
os.makedirs(data_dir, exist_ok = True)
```
:::

Sutdy species: Lupinus argenteus (silvery lupine)

::: {.cell execution_count="4"}
``` {.python .cell-code}
gbif_dir = os.path.join(data_dir, 'gbif_lupine')
```
:::

::: {.cell execution_count="5"}
``` {.python .cell-code}
reset_credentials = False

credentials = dict(
    GBIF_USER=(input, 'GBIF username:'),
    GBIF_PWD=(getpass, 'GBIF password:'),
    GBIF_EMAIL=(input, 'GBIF email:')
)
for env_variable, (prompt_func, prompt_text) in credentials.items():
    if reset_credentials and (env_variable in os.environ):
        os.environ.pop(env_variable)
    if not env_variable in os.environ:
        os.environ[env_variable] = prompt_func(prompt_text)
```
:::

Now in GBIF. Supply species code.

::: {.cell execution_count="6"}
``` {.python .cell-code}
species_name = 'Lupinus argenteus'
species_info = species.name_lookup(species_name, rank='SPECIES')
# grab first
first_result = species_info['results'][0]
species_key = first_result['nubKey']
first_result['species'], species_key
```
:::

::: {.cell execution_count="7"}
``` {.python .cell-code}
## assign species code
species_key = 2964374
```
:::

Do this once. Had trouble withing loop below so tried outside.

``` python
gbif_query = occ.download([
        f"speciesKey = {species_key}",
        "hasCoordinate = True"
    ])
gbif_query
```

::: {.cell execution_count="8"}
``` {.python .cell-code}
gbif_pattern = os.path.join(gbif_dir, '*.csv')
## download once
if not glob(gbif_pattern):
    #***with error status code 503check your number of active downloads***
    gbif_query = occ.download([
        f"speciesKey = {species_key}",
        "hasCoordinate = True"
    ])

    if not 'GBIF_DOWNLOAD_KEY' in os.environ:
        os.environ['GBIF_DOWNLOAD_KEY'] = gbif_query[0]
        download_key = os.environ['GBIF_DOWNLOAD_KEY']
        # wait for download to build
        wait = occ.download_meta(download_key)
        while not wait == 'SUCCEEDED':
            wait = occ.download_meta(download_key)['status']
            time.sleep(5)

    # download data
    # ***'function' object has no attribute 'get'***
    download_info = occ.download_get(
        os.environ['GBIF_DOWNLOAD_KEY'],
        path = data_dir
    )
    # unzip
    with zipfile.ZipFile(download_info['path']) as download_zip:
        download_zip.extractall(path = gbif_dir)

## find csv file path
gbif_path = glob(gbif_pattern)[0]
```
:::

## Katherine Notes

#### Prep workspace

::: {.cell execution_count="9"}
``` {.python .cell-code}
### load packages

### reproducible file paths
import os
from glob import glob
import pathlib

### gbif packages
import pygbif.occurrences as occ
import pygbif.species as species
from getpass import getpass

### unzipping and handling gbif data
import zipfile
import time

### deal with spatial data
import geopandas as gpd
import xrspatial

### deal with other types of data
import numpy as np
import pandas as pd
import rioxarray as rxr
import rioxarray.merge as rxrm

### invalid geometries
from shapely.geometry import MultiPolygon, Polygon

### visualizing
import holoviews as hv
import hvplot.pandas
import hvplot.xarray
```
:::

#### Prep file paths

::: {.cell execution_count="10"}
``` {.python .cell-code}
#### make reproducible file paths
data_dir = os.path.join(

    ### home directory
    pathlib.Path.home(),

    ### eda directory
    'earth-analytics',
    'data',

    ### project dir
    'hab_suit'
)

### make the dir
os.makedirs(data_dir, exist_ok=True)
```
:::

Study species: Lupinus argenteus (silvery lupine)

::: {.cell execution_count="11"}
``` {.python .cell-code}
### set gbif dir
gbif_dir = os.path.join(data_dir, 'gbif_lupine')
```
:::

::: {.cell execution_count="12"}
``` {.python .cell-code}
### access gbif
reset_credentials = False

### enter gbif username, password, and email
credentials = dict(
    GBIF_USER=(input, 'GBIF username:'),
    GBIF_PWD=(getpass, 'GBIF password'),
    GBIF_EMAIL=(input, 'GBIF email'),
)
for env_variable, (prompt_func, prompt_text) in credentials.items():

    ### delete credential from the environment if requested
    if reset_credentials and (env_variable in os.environ):
        os.environ.pop(env_variable)
    
    ### ask for credential and save to environment
    if not env_variable in os.environ:
        os.environ[env_variable] = prompt_func(prompt_text)
```
:::

#### Set up species info for GBIF

::: {.cell execution_count="13"}
``` {.python .cell-code}
### species names
species_name = 'Lupinus argenteus'

### species info for gbif
species_info = species.name_lookup(species_name, 
                                   rank = 'SPECIES')

### grab the first result
first_result = species_info['results'][0]

### get species key
species_key = first_result['nubKey']

### check on that
first_result['species'], species_key
```
:::

::: {.cell execution_count="14"}
``` {.python .cell-code}
### assign species code
species_key = 2964374
```
:::

#### Download species pccurrence data

::: {.cell execution_count="15"}
``` {.python .cell-code}
### set a file pattern
gbif_pattern = os.path.join(gbif_dir,
                            '*.csv')

### download it once
if not glob(gbif_pattern):

    ### submit my query to GBIF
    gbif_query = occ.download([
        f"speciesKey = {species_key}",
        "hasCoordinate = True",
    ])

    ### only download once
    if not 'GBIF_DOWNLOAD_KEY' in os.environ:
        os.environ['GBIF_DOWNLOAD_KEY'] = gbif_query[0]
        download_key = os.environ['GBIF_DOWNLOAD_KEY']

        ### wait for download to build
        wait = occ.download_meta(download_key)['status']
        while not wait == 'SUCCEEDED':
            wait = occ.download_meta(download_key)['status']
            time.sleep(5)
    
    ### download the data
    download_info = occ.download_get(
        os.environ['GBIF_DOWNLOAD_KEY'],
        path = data_dir
    )

    ### unzip it
    with zipfile.ZipFile(download_info['path']) as download_zip:
        download_zip.extractall(path = gbif_dir)


### find csv file path
gbif_path = glob(gbif_pattern)[0]
```
:::

#### Check out the GBIF data

::: {.cell execution_count="16"}
``` {.python .cell-code}
#### open gbif data
gbif_df = pd.read_csv(
    gbif_path,
    delimiter = '\t'
)

### take a look
gbif_df.head()
```
:::

::: {.cell execution_count="17"}
``` {.python .cell-code}
### see what the columns are
gbif_df.columns
```
:::

::: {.cell execution_count="18"}
``` {.python .cell-code}
### make it spatial
gbif_gdf = (
    gpd.GeoDataFrame(
        gbif_df,
        geometry=gpd.points_from_xy(
            gbif_df.decimalLongitude,
            gbif_df.decimalLatitude
        ),
        crs = 'EPSG:4326'
    )
)

gbif_gdf
```
:::

::: {.cell execution_count="19"}
``` {.python .cell-code}
### plot where it's found
gbif_gdf.hvplot(
    geo=True, tiles='EsriImagery',
    title = 'Silvery lupine occurrences in GBIF',
    fill_color = None, line_color = 'purple', 
    frame_width = 600
)
```
:::

## Select study sites

::: {.cell execution_count="20"}
``` {.python .cell-code}
### site directory
site_dir = os.path.join(data_dir, 'sites_lupine')
os.makedirs(site_dir, exist_ok=True)
```
:::

First manually download CA data from [Protected Areas Database
(PAD-US)](https://www.usgs.gov/programs/gap-analysis-project/science/pad-us-data-download).

::: {.cell execution_count="21"}
``` {.python .cell-code}
## open pa path
pa_path = os.path.join(site_dir, 'PADUS4_0_StateCA.gdb')

### open polygon
pa_shp = gpd.read_file(pa_path)
```
:::

::: {.cell execution_count="22"}
``` {.python .cell-code}
### check crs
print(pa_shp.crs)
```
:::

::: {.cell execution_count="23"}
``` {.python .cell-code}
### convert crs
pa_shp = pa_shp.to_crs(epsg = 4326)
```
:::

##### deal with invalid and missing geometries

::: {.cell execution_count="24"}
``` {.python .cell-code}
### fix invalid geoms
pa_shp['geometry'] = (
    pa_shp['geometry'].
    apply(lambda geom: 
        geom.make_valid() if not isinstance(geom MultiPolygon) and
        not geom.is_valid else geom)
)
```
:::

::: {.cell execution_count="25"}
``` {.python .cell-code}
### drop remaining invalid geometries
pa_shp = pa_shp[pa_shp.geometry.is_valid]
```
:::

::: {.cell execution_count="26"}
``` {.python .cell-code}
### drop rows with missing geometries
pa_shp = pa_shp.dropna(subset=['geometry'])
```
:::

::: {.cell execution_count="27"}
``` {.python .cell-code}
### plot a subset of the sites
subset_pa = pa_shp.head(50)
subset_pa.hvplot(
    geo=True, tiles='EsriImagery',
    title = 'Protected areas in California',
    fill_color = None, line_color = 'orange', 
    frame_width = 600
)
```
:::

::: {.cell execution_count="28"}
``` {.python .cell-code}
### check out the columns
pa_shp.columns
```
:::

::: {.cell execution_count="29"}
``` {.python .cell-code}
### simplify columns
pa_shp = pa_shp[['Own_Name', 'Mang_Name',
                 'Unit_Nm', 'Loc_Nm',
                 'geometry']]
```
:::

##### Option 1: select study sites by GBIF occurrences

::: {.cell execution_count="30"}
``` {.python .cell-code}
### intersect lupine occurrence with california PAs
lupine_ca = gpd.overlay(gbif_gdf, pa_shp, how = 'intersection')
```
:::

::: {.cell execution_count="31"}
``` {.python .cell-code}
### how many occurrences per site?
value_counts = lupine_ca['Loc_Nm'].value_counts()
value_counts
```
:::

##### Option 2: select study sites based on research into where the species is found

Here, I will focus on Inyo National Forest and Carrizo Plain National
Monument, two places where I have observed this species.

For Inyo, I know that I just want the rows where Loc_Nm is "Inyo
National Forest."

::: {.cell execution_count="32"}
``` {.python .cell-code}
### subset to inyo
inyo_gdf = pa_shp[pa_shp['Loc_Nm'] == 'Inyo National Forest']

### drop excess columns
inyo_gdf = inyo_gdf[['Loc_Nm', 'geometry']]

inyo_gdf
```
:::

For the Carrizo Plain, there are a couple different Loc_Nm's I might
want:

::: {.cell execution_count="33"}
``` {.python .cell-code}
### figure out which rows are Carrizo
carrizo_rows = (
    pa_shp[pa_shp['Loc_Nm']
    .str
    .contains('Carrizo', case = False, na = False)]
)
### simplify cols
carrizo_rows = carrizo_rows[['Loc_Nm', 'geometry']]

### simplify loc name
carrizo_gdf = carrizo_rows.copy()
carrizo_gdf['Loc_Nm'] = 'Carrizo Plain'

carrizo_gdf
```
:::

##### Plot them

::: {.cell execution_count="34"}
``` {.python .cell-code}
### plot inyo
inyo_gdf.dissolve().hvplot(
    geo = True, tiles = 'EsriImagery',
    title = 'Inyo National Forest',
    fill_color = None, line_color = 'darkorange',
    frame_width = 600
)
```
:::

::: {.cell execution_count="35"}
``` {.python .cell-code}
### plot carrizo
carrizo_gdf.dissolve().hvplot(
    geo = True, tiles = 'EsriImagery',
    title = 'Carrizo National Monument',
    fill_color = None, line_color = 'darkorange',
    frame_width = 600
)
```
:::

::: {.cell execution_count="36"}
``` {.python .cell-code}
### combine
sites_gdf = gpd.GeoDataFrame(pd.concat([inyo_gdf, carrizo_gdf], ignore_index = True))
sites_gdf
```
:::
