# Plot Functions

We have been using a variety of plots for a variety of data types.
It is useful to consider static and dynamic plots separately.
Static plots can be saved as PNG files and embedded in Markdown files.
Dynamic plots can be rendered interactively in Jupyter notebooks
or Quarto documents and saved as HTML files.

- [README: Package Modules and Functions](README.md#package-modules-and-functions) (Plot Data drop-down menu)
- [References: Plot Libraries and Systems](references.md#plot-libraries-and-systems)

## Static Plot Functions

The static plots are in [plots.py](plots.py).
They rely on [matplotlib](https://matplotlib.org/) and [Geopandas](https://geopandas.org/),
and sometimes [Seaborn](https://seaborn.pydata.org/).
Extensions to `matplotlib` enable creation of dynamic plots,
but we are not using them here.
Here are some of the functions we have developed so far.
These descriptions are terse,
giving key plot elements and
refering to the Jupyter notebooks or Quarto documents
where they are used.

### Plot of DataArray Objects

- `plot_index(da)`
  - [fundamentals-04-redlining-byandell/notebooks/madison.ipynb]()
  - `da.plot()` with title from `place` argument 
- `plot_das(das)`
  - [habitat-suitability-byandell/climate.qmd](https://github.com/earthlab-education/habitat-suitability-byandell/blob/main/climate.md)
  - `dai.plot()`

Plot of DataArray with GDF boundary overlay.

- `plot_gdf_da(gdf, da)`
  - [fundamentals-04-redlining-byandell/notebooks/madison.ipynb]()
  - [habitatSuitability/buffalo.qmd](https://github.com/earthlab-education/habitatSuitability/blob/main/buffalo.md)
  - [habitat-suitability-byandell/climate.qmd](https://github.com/earthlab-education/habitat-suitability-byandell/blob/main/climate.md)
  - project to Mercator
    - `da.rio.reproject(ccrs.Mercator())`
    - `gdfi = gdf.iloc[[idx]].to_crs(ccrs.Mercator())`
  - overlay gdf boundary on da
    - `da.plot()`
    - `gdfi.boundary.plot(ax=plt.gca())`

Plots of GDF with state boundary overlay and basemap.

- `plot_gdf_state(gdf)`
  - [habitatSuitability/buffalo.qmd](https://github.com/earthlab-education/habitatSuitability/blob/main/buffalo.md)
  - [habitat-suitability-byandell/climate.qmd](https://github.com/earthlab-education/habitat-suitability-byandell/blob/main/climate.md)
  - read census gdf for states and aiannh regions
  - overlay regions on gdf
    - `gdf_state.boundary.plot()`
    - `gdf_aiannh.boundary.plot()`
    - `gdf.plot()`
    - `ctx.add_basemap()` from OpenStreetMap
- `plot_gdfs_map(gdf)`
  - [big-data-byandell/big-data.qmd](https://github.com/earthlab-education/big-data-byandell/blob/main/big-data.md)
  - multiple figures in row
    - `gdfi.plot()`
    - `ctx.add_basemap()` from OpenStreetMap
- `plot_delta_gdf(gdf)`
  - [clustering-byandell/clustering.qmd]()
  - one plot
    - `gdf.plot()`
    - `ctx.add_basemap()` from OpenStreetMap

Plot of RGB DataArray

- `plot_cluster(rgb_sat, model_df)`
  - [clustering-byandell/clustering.qmd]()
  - two plots
    - reshape rgb_sat from bands (see code) to image
      - `sh = rgb_sat.shape`
      - `da = xr.DataArray(rgb_sat, dims=["band", "y", "x"], coords={"band": ["R", "G", "B"]})`
      - `df = da.stack(z=("y", "x")).transpose("z", "band").to_pandas()`
      - `img = df.values.reshape((sh[1], sh[2], 3))`
      - `ax[0].imshow(img)`
    - `model_df` has cluster labels
      - `model_df.clusters.to_xarray().sortby(['x', 'y']).plot(ax=ax[1])`

Other plots for AI model training and testing in
[big-data-byandell/big-data.qmd](https://github.com/earthlab-education/big-data-byandell/blob/main/big-data.md).

- `plot_matrix(df)`
- `plot_train_test(y_test)`

## Grammar of Graphics Plot Functions

I plan to develop functions [ggplot.py](ggplot.py) using
[Plotnine](https://plotnine.readthedocs.io/),
the Grammar of Graphics analog in Python for R's ggplot2.

## Dynamic Plot Functions

Several
[HoloViews](https://holoviews.org/)
and
[GeoViews](https://geoviews.org/)
functions have arisen and are included.
These are cool functions and easy to manipulate or render interactively,
but they generate massive image objects--Mb vs Kb for
[matplotlib.pyplot](https://matplotlib.org/stable/tutorials/pyplot.html)
similar image objects.

- [HoloViews](http://holoviews.org/)
  - [hv_plots.py](hv_plots.py)
  - [GeoViews](http://geoviews.org/)
  - [gvplot.py](gvplot.py)

In some cases, I have created simpler plot functions to generate
simpler `qmd` and `md` pages. For instance

```
#| label: fig-resid
from landmapy.plots import plot_gdfs_map
plot_gdfs_map(logndvi_cdc_gdf, column=['asthma','resid','edge_density'], color=['Blues','RdBu','Greens'])
```

generates a small (168Kb) named figure,
[big-data_files/figure-markdown/fig-resid-output-1.png](https://github.com/earthlab-education/big-data-byandell/blob/main/big-data_files/figure-markdown/fig-resid-output-1.png)
with optional accompanying figure caption (via a line `#| fig-cap: "Blah Blah"`).
An alternative is the fancier GeoViews/HoloViews,
which generates a larger (Mb) object that is embedded in the Markdown,
making it too big to render on GitHub. Here is that code:

```
import holoviews as hv
from landmapy.gvplot import gvplot_ndvi_index, gvplot_resid

model_fit = gvplot_ndvi_index(ndvi_cdc_gdf)
resid = gvplot_resid(logndvi_cdc_gdf, reg, yvar='asthma')
models_gv = (model_fit[0] + resid + model_fit[1])
hv.save(models_gv, 'bigdata_model.html')
```

While `hvplot` and `gvplot` provide interactivity, as does `matplotlib` with widgets,
there are multiple other tools that provide interactivity
that might be employed in the future:

- [Bokeh](https://bokeh.org/)
- [Folium](https://python-visualization.github.io/folium/) (Leaflet.js for Python)
- [Plotly](https://plotly.com/)
