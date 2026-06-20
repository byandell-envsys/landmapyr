# Key APIs and Data Sources in `landmapyr`

**Prompt:**
What are the key APIs that `landmapyr` uses to fetch environmental, biodiversity, and public health data? List them out and for each one, list which module(s) call that API.

**Response:**

The `landmapyr` package integrates with several major spatial data APIs and repositories to fetch environmental, biodiversity, and public health data.

### 1. Remote Sensing & Satellite Imagery

* **NASA Earthdata (CMR API)**: Used via the `earthaccess` package to search and download **Harmonized Landsat Sentinel (HLS)** imagery and **SRTM** (Shuttle Radar Topography Mission) elevation data.
* **Microsoft Planetary Computer (STAC API)**: Used via `pystac-client` to access the **NAIP** (National Agriculture Imagery Program) high-resolution aerial imagery catalog.

### 2. Biodiversity & Ecology

* **GBIF (Global Biodiversity Information Facility)**: Accessed via `pygbif` to download species occurrence data for biodiversity modeling.
* **WWF Ecoregions**: Fetches global ecoregion boundaries from Google Cloud Storage (`storage.googleapis.com/teow2016`) to provide ecological context for species data.

### 3. Public Health & Social Data

* **CDC Socrata API (data.cdc.gov)**: Used to download **PLACES** data (census tract-level health statistics like asthma prevalence) and associated Census tract geometries.
* **Mapping Inequality (University of Richmond)**: Downloads historical HOLC **redlining** data (GeoPackage format) used to analyze environmental justice and urban health.

### 4. Hydrology & Climate

* **USGS NWIS (National Water Information System)**: Accessed via the `dataretrieval` package to fetch real-time and historical streamflow, gage height, and water quality data from USGS stations.
* **THREDDS Data Server (MACA Climate)**: Used to fetch **MACA** (Multivariate Adaptive Constructed Analogs) climate projection data (e.g., precipitation scenarios) via the OPeNDAP protocol from `thredds.northwestknowledge.net`.
* **POLARIS Soil Properties**: Fetches high-resolution soil data (sand, clay, organic matter) from the Duke University hydrology server (`hydrology.cee.duke.edu`).

### 5. Administrative & Census Data

* **Census TIGER/Line**: Accesses US State and AIANNH (American Indian, Alaska Native, and Native Hawaiian) boundaries directly from Census Bureau zip archives for mapping overlays.

### Summary of API Access Points

| API / Source | Data Type | Module(s) |
| :--- | :--- | :--- |
| **NASA Earthdata** | Satellite (HLS), Elevation (SRTM) | `earthaccess.py`, `srtm.py` |
| **Planetary Computer** | Aerial Imagery (NAIP) | `naip.py` |
| **CDC Socrata** | Health Stats, Census Tracts | `cdcplaces.py` |
| **USGS NWIS** | Streamflow, Water Data | `usgs.py` |
| **GBIF** | Species Occurrences | `gbif.py` |
| **THREDDS** | Climate Projections | `thredds.py` |
| **POLARIS** | Soil Properties | `polaris.py` |
| **Mapping Inequality**| Redlining Boundaries | `redline.py` |
