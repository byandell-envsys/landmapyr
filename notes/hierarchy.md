# Module Hierarchy

**Prompt:**
Map out the hierarchy of modules in `landmapyr`. That is, which depend only on outside packages, and which depend on other modules in `landmapyr`. This will be helpful to strategize translation to R later.

**Response:**

The `landmapyr` package has a remarkably flat and modular architecture. Most modules are "leaf" modules that depend only on external spatial libraries, making them easier to translate to R individually.

### `landmapyr` Module Hierarchy

#### Level 1: Foundation Modules (No Internal Dependencies)

These modules rely solely on external Python packages (e.g., `geopandas`, `xarray`, `rioxarray`, `earthaccess`, `scikit-learn`). They can be translated first without worrying about other internal code.

| Module | Core Responsibility | Key External Dependencies |
| :--- | :--- | :--- |
| **`cached.py`** | Result caching decorator | `pickle`, `earthpy` |
| **`process.py`** | Core raster operations (masking, clipping) | `rioxarray`, `xarray`, `rasterio` |
| **`earthaccess.py`**| NASA data search and link retrieval | `earthaccess`, `geopandas` |
| **`check.py`** | Data validation (CSV headers, rows) | `pandas`, `csv` |
| **`cdcplaces.py`** | Health data and census boundaries | `geopandas`, `pandas` |
| **`gbif.py`** | Biodiversity data interface | `pygbif`, `geopandas` |
| **`redline.py`** | Redlining data acquisition | `geopandas`, `regionmask` |
| **`usgs.py`** | Streamflow data access | `dataretrieval`, `holoviews` |
| **`naip.py`** | NAIP imagery workflow | `pystac_client`, `rioxarray` |
| **`explore.py`** | Modeling and statistical exploration | `scikit-learn`, `xarray` |
| **`plots.py`** | Static visualization | `matplotlib`, `cartopy`, `contextily` |
| **`hv_plots.py`** | Interactive visualization | `hvplot`, `holoviews` |
| **`gvplot.py`** | Geoviews visualization | `geoviews`, `cartopy` |
| **`initial.py`** | Environment/Directory setup | `os`, `pathlib` |

---

#### Level 2: Mid-Level Modules (Depend on Level 1)

These modules integrate foundation logic to perform specialized spatial tasks. You should translate the Level 1 dependencies first before moving to these.

| Module | Depends On | Usage |
| :--- | :--- | :--- |
| **`srtm.py`** | `process.py` | Uses `clip_gdf_da_bounds` for elevation data. |
| **`thredds.py`** | `process.py` | Uses `clip_gdf_da_bounds` for climate data. |
| **`polaris.py`** | `process.py` | Uses `clip_gdf_da_bounds` for soil data. |
| **`reflect.py`** | `cached.py`, `earthaccess.py` | Uses `cached` for data persistence and `get_earthaccess_links` for NASA HLS data. |

---

#### Level 3: Interaction & Legacy

* **`legacy.py`**: Handles backward compatibility.
* **`__init__.py`**: Currently acts as a documentation hub for the package functions.

### Translation Strategy Tip

To successfully migrate to R:

1. **Start with `process.py`**: This is the most imported internal module. Translating its clipping and merging logic (likely into `terra` or `stars` functions) will unlock `srtm`, `thredds`, and `polaris`.
2. **Translate `cached.py`**: R alternatives like `memoise` or simple RDS-based caching will be needed for `reflect.py`.
3. **Leaf Modules**: Packages like `usgs.py` and `gbif.py` are highly independent and can be translated in any order.
