# Key Python Spatial Packages in `landmapyr`

**Prompt:**
What are the key Python packages for spatial data in `landmapyr`? Categorize them based on the type of spatial data they handle.

**Response:**

Based on an analysis of the `landmapyr` modules and the `pyproject.toml` file, the key Python packages for spatial data are categorized below:

## 1. Vector Data Handling

* **[geopandas](https://geopandas.org/)**: The primary library for handling vector data (shapefiles, GeoJSON). It is used throughout the package for managing geographic boundaries (states, cities, census tracts, ecoregions).
* **[shapely](https://shapely.readthedocs.io/)**: Used for low-level geometry manipulation and calculations, such as creating polygons and checking intersections.
* **[pyproj](https://pyproj4.github.io/pyproj/stable/)**: Used for coordinate reference system (CRS) transformations (often accessed through `geopandas`).

### 2. Raster Data Handling

* **[xarray](https://docs.xarray.dev/)**: The core engine for handling multi-dimensional spatial arrays (rasters).
* **[rioxarray](https://corteva.github.io/rioxarray/)**: An extension for `xarray` that facilitates reading GeoTIFFs, cropping rasters by vector boundaries, and managing spatial metadata.
* **[rasterio](https://rasterio.readthedocs.io/)**: The underlying library for raster data access, used in `process.py` for tasks like vectorizing rasters.

### 3. Spatial Analysis & Modeling

* **[regionmask](https://regionmask.readthedocs.io/)**: Used for creating masks from spatial regions (like ecoregions) to filter or group raster data.
* **[scipy.ndimage](https://docs.scipy.org/doc/scipy/reference/ndimage.html)**: Used in `naip.py` for advanced spatial analysis on raster data, such as patch size labeling and edge density calculations.

### 4. Data Access & APIs

* **[earthaccess](https://github.com/nsidc/earthaccess)**: Used in `earthaccess.py` to search for and download NASA Earthdata (e.g., HLS data).
* **[pystac-client](https://pystac-client.readthedocs.io/)**: Used in `naip.py` to search SpatioTemporal Asset Catalogs (STAC), specifically the Microsoft Planetary Computer, for NAIP imagery.
* **[pygbif](https://github.com/gbif/pygbif)**: Used in `gbif.py` to query and download biodiversity occurrence data from the Global Biodiversity Information Facility.

### 5. Visualization

* **[cartopy](https://scitools.org.uk/cartopy/docs/latest/)**: Used for managing map projections and coordinate transformations in plots.
* **[contextily](https://contextily.readthedocs.io/)**: Used to add web-based basemaps (like OpenStreetMap or CartoDB) to static plots.
* **[hvplot](https://hvplot.holoviz.org/) & [geoviews](https://geoviews.org/)**: Used for interactive spatial plotting (found in `hv_plots.py` and `gvplot.py`).
* **[matplotlib](https://matplotlib.org/)**: The foundational plotting library used for generating maps and diagnostic plots in `plots.py`.

### Summary Table

| Package | Primary Use in `landmapyr` |
| :--- | :--- |
| `geopandas` | Vector dataframes and spatial joins |
| `rioxarray` | Raster I/O and spatial clipping |
| `xarray` | Multi-dimensional array processing |
| `cartopy` | Map projections and CRS handling |
| `earthaccess` | Accessing NASA satellite data |
| `pystac-client`| Querying STAC catalogs (Planetary Computer) |
| `pygbif` | Accessing biodiversity data |
| `contextily` | Adding basemaps to Matplotlib plots |
