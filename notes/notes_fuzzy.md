---
execute:
  eval: false
jupyter: python3
title: Fuzzy Logic
toc-title: Table of contents
---

-   [Brian Notes](#brian-notes)
-   [Elsa Notes](#elsa-notes)

## Brian Notes

::: {.cell execution_count="1"}
``` {.python .cell-code}
conda install skfuzzy
```
:::

Libraries

::: {.cell execution_count="2"}
``` {.python .cell-code}
pip install --quiet git+https://github.com/byandell-envsys/landmapy.git
```
:::

Libraries

::: {.cell execution_count="3"}
``` {.python .cell-code}
from math import floor, ceil
import cartopy.crs as ccrs
import geopandas as gpd
import hvplot.pandas
import hvplot.xarray
import numpy as np
import rioxarray as rxr
import rioxarray.merge as rxrmerge
import skfuzzy
import xarray as xr
```
:::

My version:

``` python
from landmapy.initial import create_data_dir # create (or retrieve) data directory
from landmapy.plot import plot_gdf_state # plot gdf with state overlay

%store -r buffalo_gdf
try:
    buffalo_gdf
except NameError:
    data_dir = create_data_dir('habitat')
    # Read all grasslands GeoJSON into `grassland_gdf`.
    grassland_url = f"{data_dir}/National_Grassland_Units_(Feature_Layer).geojson"
    grassland_gdf = gpd.read_file(grassland_url)
    # Subset to desired locations.
    buffalo_gdf = grassland_gdf.loc[grassland_gdf['GRASSLANDNAME'].isin(
        ["Buffalo Gap National Grassland", "Oglala National Grassland"])]
    %store buffalo_gdf
    print("buffalo_gdf created and stored")
else:
    print("buffalo_gdf retrieved from StoreMagic")
```

Elsa's version

::: {.cell execution_count="4"}
``` {.python .cell-code}
grassland_url = (
    "https://data.fs.usda.gov/geodata/edw/edw_resources/shp/S_USA.NationalGrassland.zip")
grassland_gdf = gpd.read_file(grassland_url)
grassland_gdf.info
```
:::

::: {.cell execution_count="5"}
``` {.python .cell-code}
oglala_gdf = grassland_gdf[grassland_gdf.GRASSLANDN.str.contains('Oglala')]
(
    oglala_gdf
    .to_crs(ccrs.Mercator())
    .hvplot(tiles='EsriNatGeo', line_width=3, fill_color=None)
)
```
:::

::: {.cell execution_count="6"}
``` {.python .cell-code}
oglala_gdf
```
:::

::: {.cell execution_count="7"}
``` {.python .cell-code}
from landmapy.polaris import merge_soil

ph_da = merge_soil(oglala_gdf, "ph", "mean", "60_100", 0.1)
ph_da.plot()
```
:::

::: {.cell execution_count="8"}
``` {.python .cell-code}
from landmapy.thredds import process_maca

maca_df = process_maca({'oglala': oglala_gdf}, ['pr'], ['rcp45'], (2011, 2040))
```
:::

This part differs from Elsa's demo. She ended her loop with (ignoring
buffer) `periods.append(period_da)`, so there is just the DataArray
`periods`.

For the Fall project, I constructed (in `process_maca()`) I did
`maca_da_list.append(dict(..., da = maca_da))` so that the DataArray
ended up as part of the `dict()`. Then I converted to a DataFrame
`maca_df = pd.DataFrame(maca_da_list)`. To pull out the DataFrame `da`
requires the following step:

::: {.cell execution_count="9"}
``` {.python .cell-code}
maca0_da = maca_df.loc[1, 'da']
```
:::

::: {.cell execution_count="10"}
``` {.python .cell-code}
maca_da = (
    xr.concat(maca_df['da'].tolist(), dim='five_year')
    .isel(five_year=0)
)
```
:::

I checked with the following code that the dimension 'five_year' appears
to be redundant. Hoping this is true.

``` python
maca_da = xr.concat(maca_df['da'].tolist(), dim='five_year')
m0 = maca_da.isel(five_year=0)
m1 = maca_da.isel(five_year=2)
(m0-m1).sum()
```

::: {.cell execution_count="11"}
``` {.python .cell-code}
print(maca0_da.dims)
print(maca0_da.shape)
print(maca_da.dims)
print(maca_da.shape)
```
:::

Sum over time within each year over the 30 years ('time'), reprojecting
to shape of `ph_da`.

::: {.cell execution_count="12"}
``` {.python .cell-code}
precip_da = (
    xr.concat(maca_da, dim='time')
    .resample({'time': 'YE'})
    .sum()
    .rio.write_crs(4236) 
    .rio.reproject_match(ph_da)
)
```
:::

::: {.cell execution_count="13"}
``` {.python .cell-code}
print(precip_da.shape)
print(precip_da.dims)
```
:::

::: {.cell execution_count="14"}
``` {.python .cell-code}
precip_min_da = precip_da.min('time')
precip_max_da = precip_da.max('time')
precip_mean_da = precip_da.mean('time')
```
:::

::: {.cell execution_count="15"}
``` {.python .cell-code}
precip_mean_da.plot()
```
:::

::: {.cell execution_count="16"}
``` {.python .cell-code}
precip_min_da.plot()
```
:::

::: {.cell execution_count="17"}
``` {.python .cell-code}
precip_max_da.plot()
```
:::

Precipitation in mm. (11-45in = 279-1143mm)

### Non-fuzzy logic model

::: {.cell execution_count="18"}
``` {.python .cell-code}
((precip_mean_da > 95) & (precip_max_da < 800)).plot()
```
:::

::: {.cell execution_count="19"}
``` {.python .cell-code}
precip_min_da.plot.hist()
```
:::

### Fuzzy logic

[trimf](https://scikit-fuzzy.readthedocs.io/en/latest/api/skfuzzy.html?highlight=trimf#skfuzzy.trimf)
is triangle. It takes a 1-D array, but we have 2-D array

::: {.cell execution_count="20"}
``` {.python .cell-code}
ph = [4.8, 8]
tri = [ph[0], (ph[0] + ph[1])/2, ph[1]]
shape = ph_da.values.shape
ph_fuzz = ph_da.copy()
ph_fuzz.values = (
    np.reshape(
        skfuzzy.trimf(ph_da.values.flatten(), tri),
    shape)
)
ph_fuzz.plot()
```
:::

::: {.cell execution_count="21"}
``` {.python .cell-code}
trap = [ph[0], (2 * ph[0] + ph[1])/3, (ph[0] + 2 * ph[1]) /3, ph[1]]
shape = ph_da.values.shape
ph_fuzz = ph_da.copy()
ph_fuzz.values = (
    np.reshape(
        skfuzzy.trapmf(ph_da.values.flatten(), trap),
    shape)
)
ph_fuzz.plot()
```
:::

::: {.cell execution_count="22"}
``` {.python .cell-code}
pr = [310, 700]
trap = [pr[0], (2 * pr[0] + pr[1])/3, (pr[0] + 2 * pr[1]) /3, pr[1]]
shape = precip_min_da.values.shape
precip_fuzz = precip_min_da.copy()
precip_fuzz.values = (
    np.reshape(
        skfuzzy.trapmf(precip_min_da.values.flatten(), trap),
    shape)
)
precip_fuzz.plot()
```
:::

[dsw_mult](https://scikit-fuzzy.readthedocs.io/en/latest/api/skfuzzy.html?highlight=dsw_mult#skfuzzy.dsw_mult)

but could use regular mult

::: {.cell execution_count="23"}
``` {.python .cell-code}
(ph_fuzz * precip_fuzz).plot(robust=True)
```
:::

::: {.cell execution_count="24"}
``` {.python .cell-code}
((ph_fuzz * precip_fuzz) > 0.05).plot()
```
:::

## Elsa Notes

Created by [Elsa Culler](https://github.com/eculler) for 27 Feb 2025
[video on Fuzzy
Logic](https://cuboulder.zoom.us/rec/play/EnTi2FyvDddFKN86INR7iypERZ59IHE5xxZXSS3R9vQAjJ4RczjpwYqFa63JhF9Hdq1Dv9U1iVZX65Vw.qfKwpud-sV9GAqKp).
Slightly adapted after `quarto convert habitat_example.ipynb` to Quarto.

Sorghastrum nutans is found in the entire U.S. east of the rocky
mountains, but seems to be concentrated in the southeast and moving
northward over time. Generally found in tallgrass prairies.

  Value                  Min   Max
  ---------------------- ----- -----
  Annual precipitation   11    45
  pH                     4.8   8.0

USDA Natural Resources Conservations Service. Plant Guide: Indiangrass.
Accessed February 26, 2025 from
https://data.fs.usda.gov/geodata/edw/edw_resources/shp/S_USA.NationalGrassland.zip

For soil data: rooting depth averages around 70 cm.

Brown, R. N., Percivalle, C., Narkiewicz, S., & DeCuollo, S. (2010).
Relative Rooting Depths of Native Grasses and Amenity Grasses with
Potential for Use on Roadsides in New England. HortScience horts, 45(3),
393-400. Retrieved Feb 26, 2025, from
https://doi.org/10.21273/HORTSCI.45.3.393

::: {.cell execution_count="25"}
``` {.python .cell-code}
#%conda install skfuzzy
```
:::

::: {.cell execution_count="26"}
``` {.python .cell-code}
from math import floor, ceil

import cartopy.crs as ccrs
import geopandas as gpd
import hvplot.pandas
import hvplot.xarray
import numpy as np
import rioxarray as rxr
import rioxarray.merge as rxrmerge
import skfuzzy
import xarray as xr
```
:::

::: {.cell execution_count="27"}
``` {.python .cell-code}
grassland_url = (
    "https://data.fs.usda.gov/geodata/edw/edw_resources/shp"
    "/S_USA.NationalGrassland.zip")
grassland_gdf = gpd.read_file(grassland_url)
grassland_gdf.info()
```
:::

## Site description

I picked the Oglala grassland for this example because it is a
mixed-grass prairie closer to the edge of sorghastrum nutans' domain.
This makes it marginal habitat for this grass species, and more likely
we'll see climate-related changes.

::: {.cell execution_count="28"}
``` {.python .cell-code}
oglala_gdf = grassland_gdf[grassland_gdf.GRASSLANDN.str.contains('Oglala')]
(
    oglala_gdf
    .to_crs(ccrs.Mercator())
    .hvplot(tiles='EsriNatGeo', line_width=3, fill_color=None)
)
```
:::

::: {.cell execution_count="29"}
``` {.python .cell-code}
xmin, ymin, xmax, ymax = oglala_gdf.total_bounds
tiles = []
for lat_min in range(floor(ymin), ceil(ymax)):
    for lon_min in range(floor(xmin), ceil(xmax)):
        lat_max, lon_max = lat_min + 1, lon_min + 1
        ph_url = (
            "http://hydrology.cee.duke.edu/POLARIS/PROPERTIES/v1.0"
            "/ph/mean/60_100"
            f"/lat{lat_min}{lat_max}_lon{lon_min}{lon_max}.tif")
        tiles.append(rxr.open_rasterio(ph_url))

ph_da = rxrmerge.merge_arrays(tiles).rio.clip_box(*oglala_gdf.total_bounds)
ph_da.plot()
```
:::

::: {.cell execution_count="30"}
``` {.python .cell-code}
year_min, year_max = 2011, 2040
model = "BNU-ESM"
emissions = 'rcp45'
variable = 'pr'
periods = []
buffer_bounds = None
for start_year in range(year_min, year_max, 5):
    end_year = start_year + 4
    climate_url = (
        "http://thredds.northwestknowledge.net:8080/thredds/dodsC/MACAV2"
        f"/{model}/macav2metdata_{variable}_{model}_r1i1p1_{emissions}"
        f"_{start_year}_{end_year}_CONUS_monthly.nc")
    period_da = (
        xr.open_dataset(climate_url, mask_and_scale=True)
        .squeeze()
        .precipitation)
    period_da = period_da.assign_coords(lon=(period_da.lon + 180) % 360 - 180)
    period_da = period_da.rio.set_spatial_dims(x_dim='lon', y_dim='lat')
    if buffer_bounds is None:
        oglala_gdf_reproj = oglala_gdf.to_crs(period_da.rio.crs)
        xmin, ymin, xmax, ymax = oglala_gdf_reproj.total_bounds
        b = .1
        buffer_bounds = [xmin - b, ymin - b, xmax + b, ymax + b]
    periods.append(period_da.rio.clip_box(*buffer_bounds))
```
:::

::: {.cell execution_count="31"}
``` {.python .cell-code}
precip_da = (
    xr.concat(periods, dim='time')
    .resample({'time': 'Y'})
    .sum()
    .rio.write_crs(4326)
    .rio.reproject_match(ph_da))

precip_min_da = precip_da.min('time')
precip_max_da = precip_da.max('time')
precip_mean_da = precip_da.mean('time')
precip_mean_da.plot()
```
:::

::: {.cell execution_count="32"}
``` {.python .cell-code}
precip_min_da.plot.hist()
```
:::

::: {.cell execution_count="33"}
``` {.python .cell-code}
# precip 11-45 (in) 279-1143
# ph 4.8-8
precip_suit = ((precip_min_da > 310) & (precip_max_da < 825))
ph_suit = ((precip_min_da > 4.8) & (precip_min_da < 8))
```
:::

::: {.cell execution_count="34"}
``` {.python .cell-code}
precip_suit.plot()
```
:::

::: {.cell execution_count="35"}
``` {.python .cell-code}
(precip_suit * ph_suit).plot()
```
:::

::: {.cell execution_count="36"}
``` {.python .cell-code}
ph_da.values
```
:::

::: {.cell execution_count="37"}
``` {.python .cell-code}
shape = ph_da.values.shape
ph_fuzz = ph_da.copy()
ph_fuzz.values = (
    np.reshape(
        skfuzzy.trimf(ph_da.values.flatten(), [4.8, (4.8 + 8)/2, 8]),
        shape)
)
ph_fuzz.plot()
```
:::

::: {.cell execution_count="38"}
``` {.python .cell-code}
shape = precip_min_da.values.shape
precip_min_fuzz = precip_min_da.copy()
precip_min_fuzz.values = (
    np.reshape(
        skfuzzy.trimf(precip_min_da.values.flatten(), 
                      [310, (310 + 825)/2, 825]),
        shape)
)
precip_min_fuzz.plot()
```
:::

::: {.cell execution_count="39"}
``` {.python .cell-code}
((ph_fuzz * precip_min_fuzz) > .05).plot()
```
:::
