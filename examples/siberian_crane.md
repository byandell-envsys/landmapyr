---
jupyter: python3
title: Access locations and times of Veery encounters
toc-title: Table of contents
---

For this challenge, you will use a database called the [Global
Biodiversity Information Facility (GBIF)](https://www.gbif.org/). GBIF
is compiled from species observation data all over the world, and
includes everything from museum specimens to photos taken by citizen
scientists in their backyards.

**Explore GBIF:** Before your get started, go to the [GBIF occurrences
search page](https://www.gbif.org/occurrence/search) and explore the
data.

See also:

-   [Crane Maps](https://github.com/byandell-envsys/craneMaps)
-   [Sandhill
    Crane](https://github.com/earthlab-education/species-distribution-coding-challenge-byandell/blob/main/notebooks/sandhill_crane.qmd)

> **Contribute to open data**
>
> You can get your own observations added to GBIF using
> [iNaturalist](https://www.inaturalist.org/)!

### Set up your code to prepare for download

We will be getting data from a source called [GBIF (Global Biodiversity
Information Facility)](https://www.gbif.org/). We need a package called
`pygbif` to access the data, which may not be included in your
environment. Install it by running the cell below:

::: {.cell execution_count="1"}
``` {.python .cell-code}
conda list pygbif
```
:::

::: {.cell execution_count="2"}
``` {.python .cell-code}
%pip install -q --upgrade git+https://github.com/byandell-envsys/landmapy.git
```
:::

::: {.cell execution_count="3"}
``` {.python .cell-code}
from landmapy.initial import create_data_dir, robust_code
from landmapy.gbif import gbif_credentials, gbif_species_key
from landmapy.gbif import download_gbif, load_gbif, gbif_monthly
from landmapy.gbif import ecoregions, join_ecoregions_monthly
from landmapy.gbif import count_by_ecoregions
from landmapy.gbif import simplify_ecoregions_gdf, join_occurrence
from landmapy.hv_plots import hvplot_occurrence
```
:::

**Import packages:** In the imports cell, we've included some packages
that you will need. Add imports for packages that will help you:

-   Work with reproducible file paths
-   Work with tabular data

:::: {.cell highlight="true" execution_count="4"}
``` {.python .cell-code}
robust_code()
data_dir = create_data_dir('species')
gbif_dir = create_data_dir('species/gbif_siberian')
gbif_dir
```

::: {.cell-output .cell-output-display execution_count="18"}
    '/Users/brianyandell/earth-analytics/data/species/gbif_siberian'
:::
::::

### Register and log in to GBIF

You will need a [GBIF account](https://www.gbif.org/) to complete this
challenge. You can use your GitHub account to authenticate with GBIF.
Then, run the following code to save your credentials on your computer.

> **Warning**
>
> Your email address **must** match the email you used to sign up for
> GBIF!

> **Tip**
>
> If you accidentally enter your credentials wrong, you can set
> `reset_credentials=True` instead of `reset_credentials=False`. Look to
> top of screen for entry of credentials.

::: {.cell execution_count="5"}
``` {.python .cell-code}
gbif_credentials(False)
```
:::

### Get the species key

> \*\* Your task\*\*
>
> 1.  Replace the `species_name` with the name of the species you want
>     to look up
> 2.  Run the code to get the species key

:::: {.cell execution_count="6"}
``` {.python .cell-code}
species_name, species_key = gbif_species_key('grus leucogeranus')
species_name, species_key
```

::: {.cell-output .cell-output-display execution_count="19"}
    ('Grus leucogeranus', 2474961)
:::
::::

### Download data from GBIF

::: {.callout-task title="Submit a request to GBIF"

1.  Replace `csv_file_pattern` with a string that will match **any**
    `.csv` file when used in the `glob` function. HINT: the character
    `*` represents any number of any values except the file separator
    (e.g. `/`)

2.  Add parameters to the GBIF download function, `occ.download()` to
    limit your query to:

    -   observations
    -   from 2023
    -   with spatial coordinates.

3.  Then, run the download. **This can take a few minutes**.

    -   Can check progress at <https://www.gbif.org/user/download>. :::

:::: {.cell execution_count="7"}
``` {.python .cell-code}
gbif_path = download_gbif(gbif_dir, species_key, year=None)
gbif_path
```

::: {.cell-output .cell-output-display execution_count="20"}
    '/Users/brianyandell/earth-analytics/data/species/gbif_siberian/0001177-250227182400228.zip'
:::
::::

    INFO:Your download key is 0001177-250227182400228
    INFO:Download file size: 171492 bytes
    INFO:On disk at /Users/brianyandell/earth-analytics/data/species/gbif_siberian/0001177-250227182400228.zip

### Load the GBIF data into Python

**Load GBIF data:**

-   Look at the beginning of the file you downloaded using the code
    below. What do you think the `delimiter` is?
-   Run the following code cell. What happens?
-   Uncomment and modify the parameters of `pd.read_csv()` below until
    your data loads successfully and you have only the columns you want.

You can use the following code to look at the beginning of your file:

I copied from [Lauren
Alexandra](https://github.com/lauren-alexandra/lauren-alexandra.github.io/blob/main/willow-flycatcher-distribution/willow-flycatcher-distribution.ipynb)
and Lauren Gleason

:::: {.cell execution_count="8"}
``` {.python .cell-code}
gbif_df = load_gbif(gbif_path)
print(gbif_df.head())
```

::: {.cell-output .cell-output-stdout}
              countryCode stateProvince  decimalLatitude  decimalLongitude  month  \
    gbifID                                                                          
    985829831          IN     Rajasthan        27.161905         77.522800    2.0   
    979229641          CN       Jiangxi        28.870571        116.433170   11.0   
    978902062          IR    Mazandaran        36.667110         52.550186   11.0   
    978782158          IN     Rajasthan        27.161905         77.522800    1.0   
    977810003          IN     Rajasthan        27.161905         77.522800    1.0   

                 year  
    gbifID             
    985829831  1991.0  
    979229641  1988.0  
    978902062  2011.0  
    978782158  1991.0  
    977810003  1992.0  
:::
::::

## Convert GBIF data to a GeoDataFrame by Month

:::: {.cell execution_count="9"}
``` {.python .cell-code}
monthly_gdf = gbif_monthly(gbif_df)
monthly_gdf
```

::: {.cell-output .cell-output-display execution_count="22"}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

               year     month   geometry
  ------------ -------- ------- ----------------------------
  gbifID                        
  985829831    1991.0   2.0     POINT (77.5228 27.1619)
  979229641    1988.0   11.0    POINT (116.43317 28.87057)
  978902062    2011.0   11.0    POINT (52.55019 36.66711)
  978782158    1991.0   1.0     POINT (77.5228 27.1619)
  977810003    1992.0   1.0     POINT (77.5228 27.1619)
  \...         \...     \...    \...
  1019036144   1983.0   6.0     POINT (-90 43.75)
  1019036117   1983.0   6.0     POINT (-90 43.75)
  1019036092   1983.0   6.0     POINT (-90 43.75)
  1019036069   1983.0   6.0     POINT (-90 43.75)
  1019035937   1983.0   6.0     POINT (-90 43.75)

<p>2936 rows × 3 columns</p>
</div>
:::
::::

### Download and save ecoregion boundaries

Ecoregions represent boundaries formed by biotic and abiotic conditions:
geology, landforms, soils, vegetation, land use, wildlife, climate, and
hydrology.

:::: {.cell execution_count="10"}
``` {.python .cell-code}
ecoregions_gdf = ecoregions(data_dir)
ecoregions_gdf.plot(edgecolor='black', color='skyblue')
```

::: {.cell-output .cell-output-display}
![](siberian_crane_files/figure-markdown/cell-11-output-1.png)
:::
::::

::: {.cell execution_count="11"}
``` {.python .cell-code}
%%bash
find ~/earth-analytics/data/species -name '*.shp'
```
:::

:::: {.cell execution_count="12"}
``` {.python .cell-code}
%store ecoregions_gdf monthly_gdf
```

::: {.cell-output .cell-output-stdout}
    Stored 'ecoregions_gdf' (GeoDataFrame)
    Stored 'monthly_gdf' (GeoDataFrame)
:::
::::

Identify the ecoregion for each observation

:::: {.cell execution_count="13"}
``` {.python .cell-code}
gbif_ecoregion_gdf = join_ecoregions_monthly(ecoregions_gdf, monthly_gdf)
gbif_ecoregion_gdf
```

::: {.cell-output .cell-output-display execution_count="25"}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

              year     month   name
  ----------- -------- ------- --------------------------------------------------
  ecoregion                    
  5           2015.0   3.0     Al-Hajar foothill xeric woodlands and shrublands
  5           2015.0   3.0     Al-Hajar foothill xeric woodlands and shrublands
  5           2014.0   7.0     Al-Hajar foothill xeric woodlands and shrublands
  5           2017.0   12.0    Al-Hajar foothill xeric woodlands and shrublands
  8           NaN      NaN     Alashan Plateau semi-desert
  \...        \...     \...    \...
  802         2023.0   1.0     Yellow Sea saline meadow
  802         2018.0   1.0     Yellow Sea saline meadow
  802         2015.0   2.0     Yellow Sea saline meadow
  802         2018.0   1.0     Yellow Sea saline meadow
  802         2015.0   1.0     Yellow Sea saline meadow

<p>2269 rows × 3 columns</p>
</div>
:::
::::

Count the observations in each ecoregion each year and month

:::: {.cell execution_count="14"}
``` {.python .cell-code}
occurrence_month_df = count_by_ecoregions(gbif_ecoregion_gdf,
                        'ecoregion', 'name', 'month')
occurrence_month_df
```

::: {.cell-output .cell-output-display execution_count="26"}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

                      occurrences   norm_occurrences
  ----------- ------- ------------- ------------------
  ecoregion   month                 
  5           3.0     2             0.098214
  24          5.0     6             0.156250
              9.0     2             0.142857
  53          3.0     9             0.098214
  74          1.0     3             0.016181
  \...        \...    \...          \...
  758         5.0     20            0.132275
              6.0     16            0.066253
  802         1.0     4             0.021575
              2.0     3             0.025840
              12.0    2             0.013605

<p>78 rows × 2 columns</p>
</div>
:::
::::

:::: {.cell execution_count="15"}
``` {.python .cell-code}
occurrence_year_df = count_by_ecoregions(gbif_ecoregion_gdf,
                        'ecoregion', 'name', 'year')
occurrence_year_df
```

::: {.cell-output .cell-output-display execution_count="27"}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

                       occurrences   norm_occurrences
  ----------- -------- ------------- ------------------
  ecoregion   year                   
  5           2015.0   2             0.194444
  24          2014.0   2             0.156250
              2017.0   2             0.065868
              2024.0   2             0.092593
  53          2020.0   4             0.059259
  \...        \...     \...          \...
  758         1996.0   3             0.084746
  802         2014.0   2             0.125000
              2015.0   3             0.233333
              2018.0   3             0.038462
              2023.0   2             0.032520

<p>140 rows × 2 columns</p>
</div>
:::
::::

:::: {.cell execution_count="16"}
``` {.python .cell-code}
# plot to check distrubions 
occurrence_year_df.reset_index().plot.scatter(
    x='year', y='occurrences', c='ecoregion',
    logy=True
)
```

::: {.cell-output .cell-output-display}
![](siberian_crane_files/figure-markdown/cell-17-output-1.png)
:::
::::

Create a simplified GeoDataFrame for plot

:::: {.cell execution_count="17"}
``` {.python .cell-code}
ecoregions_gdf = simplify_ecoregions_gdf(ecoregions_gdf)
ecoregions_gdf
```

::: {.cell-output .cell-output-display execution_count="29"}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

              name                                                 area        geometry
  ----------- ---------------------------------------------------- ----------- ----------------------------------------------------
  ecoregion                                                                    
  0           Adelie Land tundra                                   0.038948    MULTIPOLYGON EMPTY
  1           Admiralty Islands lowland rain forests               0.170599    POLYGON ((16411777.375 -229101.376, 16384825.7\...
  2           Aegean and Western Turkey sclerophyllous and m\...   13.844952   MULTIPOLYGON (((3391149.749 4336064.109, 33846\...
  3           Afghan Mountains semi-desert                         1.355536    MULTIPOLYGON (((7369001.698 4093509.259, 73168\...
  4           Ahklun and Kilbuck Upland Tundra                     8.196573    MULTIPOLYGON (((-17930832.005 8046779.358, -17\...
  \...        \...                                                 \...        \...
  842         Sulawesi lowland rain forests                        9.422097    MULTIPOLYGON (((14113374.546 501721.962, 14128\...
  843         East African montane forests                         5.010930    MULTIPOLYGON (((4298787.669 -137583.786, 42727\...
  844         Eastern Arc forests                                  0.890325    MULTIPOLYGON (((4267432.68 -493759.165, 428533\...
  845         Borneo montane rain forests                          9.358407    MULTIPOLYGON (((13126956.393 539092.917, 13136\...
  846         Kinabalu montane alpine meadows                      0.352694    POLYGON ((12981819.186 696445.445, 12997053.80\...

<p>847 rows × 3 columns</p>
</div>
:::
::::

Mapping yearly distribution

:::: {.cell execution_count="18"}
``` {.python .cell-code}
occurrence_gdf = join_occurrence(ecoregions_gdf, occurrence_year_df)
occurrence_gdf
```

::: {.cell-output .cell-output-display execution_count="30"}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

                       name                                               area        geometry                                             norm_occurrences
  ----------- -------- -------------------------------------------------- ----------- ---------------------------------------------------- ------------------
  ecoregion   year                                                                                                                         
  5           2015.0   Al-Hajar foothill xeric woodlands and shrublands   4.099668    POLYGON ((6264504.021 2842331.306, 6336024.085\...   0.194444
  24          2014.0   Amur meadow steppe                                 15.118769   MULTIPOLYGON (((15067649.194 6001589.024, 1503\...   0.156250
              2017.0   Amur meadow steppe                                 15.118769   MULTIPOLYGON (((15067649.194 6001589.024, 1503\...   0.065868
              2024.0   Amur meadow steppe                                 15.118769   MULTIPOLYGON (((15067649.194 6001589.024, 1503\...   0.092593
  53          2020.0   Azerbaijan shrub desert and steppe                 6.794797    POLYGON ((5427403.54 5089371.081, 5512543.361 \...   0.059259
  \...        \...     \...                                               \...        \...                                                 \...
  758         1996.0   Upper Midwest US forest-savanna transition         15.481685   MULTIPOLYGON (((-9686382.157 5638236.966, -973\...   0.084746
  802         2014.0   Yellow Sea saline meadow                           0.517810    POLYGON ((13451648.07 3834357.593, 13303152.21\...   0.125000
              2015.0   Yellow Sea saline meadow                           0.517810    POLYGON ((13451648.07 3834357.593, 13303152.21\...   0.233333
              2018.0   Yellow Sea saline meadow                           0.517810    POLYGON ((13451648.07 3834357.593, 13303152.21\...   0.038462
              2023.0   Yellow Sea saline meadow                           0.517810    POLYGON ((13451648.07 3834357.593, 13303152.21\...   0.032520

<p>140 rows × 4 columns</p>
</div>
:::
::::

:::::::::: {.cell execution_count="19"}
``` {.python .cell-code}
occurrence_hvplot = hvplot_occurrence(occurrence_gdf, 'year')
occurrence_hvplot
```

::: {.cell-output .cell-output-display}
<script type="esms-options">{"shimMode": true}</script><style>*[data-root-id],
*[data-root-id] > * {
  box-sizing: border-box;
  font-family: var(--jp-ui-font-family);
  font-size: var(--jp-ui-font-size1);
  color: var(--vscode-editor-foreground, var(--jp-ui-font-color1));
}

/* Override VSCode background color */
.cell-output-ipywidget-background:has(
    > .cell-output-ipywidget-background > .lm-Widget > *[data-root-id]
  ),
.cell-output-ipywidget-background:has(> .lm-Widget > *[data-root-id]) {
  background-color: transparent !important;
}
</style>
:::

::: {.cell-output .cell-output-display}
    Unable to display output for mime type(s): application/javascript, application/vnd.holoviews_load.v0+json
:::

::: {.cell-output .cell-output-display}
    Unable to display output for mime type(s): application/javascript, application/vnd.holoviews_load.v0+json
:::

::: {.cell-output .cell-output-display}
<div id='f3ab0bbd-7360-4d9b-bf37-8db4ff3f72d2'>
  <div id="c1719b79-f2b9-4c17-9587-c406cf428206" data-root-id="f3ab0bbd-7360-4d9b-bf37-8db4ff3f72d2" style="display: contents;"></div>
</div>
<script type="application/javascript">(function(root) {
  var docs_json = {"f25b880d-e767-4250-a43b-a9d42049f20a":{"version":"3.5.2","title":"Bokeh Application","roots":[{"type":"object","name":"panel.models.browser.BrowserInfo","id":"f3ab0bbd-7360-4d9b-bf37-8db4ff3f72d2"},{"type":"object","name":"panel.models.comm_manager.CommManager","id":"5f798d73-e7e7-47af-9df1-3e3efb864826","attributes":{"plot_id":"f3ab0bbd-7360-4d9b-bf37-8db4ff3f72d2","comm_id":"cbe1542046004a928e03ec830a879ccd","client_comm_id":"22f3d2963b86445585bd1293f2486b11"}}],"defs":[{"type":"model","name":"ReactiveHTML1"},{"type":"model","name":"FlexBox1","properties":[{"name":"align_content","kind":"Any","default":"flex-start"},{"name":"align_items","kind":"Any","default":"flex-start"},{"name":"flex_direction","kind":"Any","default":"row"},{"name":"flex_wrap","kind":"Any","default":"wrap"},{"name":"gap","kind":"Any","default":""},{"name":"justify_content","kind":"Any","default":"flex-start"}]},{"type":"model","name":"FloatPanel1","properties":[{"name":"config","kind":"Any","default":{"type":"map"}},{"name":"contained","kind":"Any","default":true},{"name":"position","kind":"Any","default":"right-top"},{"name":"offsetx","kind":"Any","default":null},{"name":"offsety","kind":"Any","default":null},{"name":"theme","kind":"Any","default":"primary"},{"name":"status","kind":"Any","default":"normalized"}]},{"type":"model","name":"GridStack1","properties":[{"name":"mode","kind":"Any","default":"warn"},{"name":"ncols","kind":"Any","default":null},{"name":"nrows","kind":"Any","default":null},{"name":"allow_resize","kind":"Any","default":true},{"name":"allow_drag","kind":"Any","default":true},{"name":"state","kind":"Any","default":[]}]},{"type":"model","name":"drag1","properties":[{"name":"slider_width","kind":"Any","default":5},{"name":"slider_color","kind":"Any","default":"black"},{"name":"value","kind":"Any","default":50}]},{"type":"model","name":"click1","properties":[{"name":"terminal_output","kind":"Any","default":""},{"name":"debug_name","kind":"Any","default":""},{"name":"clears","kind":"Any","default":0}]},{"type":"model","name":"FastWrapper1","properties":[{"name":"object","kind":"Any","default":null},{"name":"style","kind":"Any","default":null}]},{"type":"model","name":"NotificationAreaBase1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0}]},{"type":"model","name":"NotificationArea1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"notifications","kind":"Any","default":[]},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0},{"name":"types","kind":"Any","default":[{"type":"map","entries":[["type","warning"],["background","#ffc107"],["icon",{"type":"map","entries":[["className","fas fa-exclamation-triangle"],["tagName","i"],["color","white"]]}]]},{"type":"map","entries":[["type","info"],["background","#007bff"],["icon",{"type":"map","entries":[["className","fas fa-info-circle"],["tagName","i"],["color","white"]]}]]}]}]},{"type":"model","name":"Notification","properties":[{"name":"background","kind":"Any","default":null},{"name":"duration","kind":"Any","default":3000},{"name":"icon","kind":"Any","default":null},{"name":"message","kind":"Any","default":""},{"name":"notification_type","kind":"Any","default":null},{"name":"_destroyed","kind":"Any","default":false}]},{"type":"model","name":"TemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"BootstrapTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"TemplateEditor1","properties":[{"name":"layout","kind":"Any","default":[]}]},{"type":"model","name":"MaterialTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"ReactiveESM1","properties":[{"name":"esm_constants","kind":"Any","default":{"type":"map"}}]},{"type":"model","name":"JSComponent1","properties":[{"name":"esm_constants","kind":"Any","default":{"type":"map"}}]},{"type":"model","name":"ReactComponent1","properties":[{"name":"esm_constants","kind":"Any","default":{"type":"map"}}]},{"type":"model","name":"AnyWidgetComponent1","properties":[{"name":"esm_constants","kind":"Any","default":{"type":"map"}}]},{"type":"model","name":"request_value1","properties":[{"name":"fill","kind":"Any","default":"none"},{"name":"_synced","kind":"Any","default":null},{"name":"_request_sync","kind":"Any","default":0}]}]}};
  var render_items = [{"docid":"f25b880d-e767-4250-a43b-a9d42049f20a","roots":{"f3ab0bbd-7360-4d9b-bf37-8db4ff3f72d2":"c1719b79-f2b9-4c17-9587-c406cf428206"},"root_ids":["f3ab0bbd-7360-4d9b-bf37-8db4ff3f72d2"]}];
  var docs = Object.values(docs_json)
  if (!docs) {
    return
  }
  const py_version = docs[0].version.replace('rc', '-rc.').replace('.dev', '-dev.')
  async function embed_document(root) {
    var Bokeh = get_bokeh(root)
    await Bokeh.embed.embed_items_notebook(docs_json, render_items);
    for (const render_item of render_items) {
      for (const root_id of render_item.root_ids) {
    const id_el = document.getElementById(root_id)
    if (id_el.children.length && id_el.children[0].hasAttribute('data-root-id')) {
      const root_el = id_el.children[0]
      root_el.id = root_el.id + '-rendered'
      for (const child of root_el.children) {
            // Ensure JupyterLab does not capture keyboard shortcuts
            // see: https://jupyterlab.readthedocs.io/en/4.1.x/extension/notebook.html#keyboard-interaction-model
        child.setAttribute('data-lm-suppress-shortcuts', 'true')
      }
    }
      }
    }
  }
  function get_bokeh(root) {
    if (root.Bokeh === undefined) {
      return null
    } else if (root.Bokeh.version !== py_version) {
      if (root.Bokeh.versions === undefined || !root.Bokeh.versions.has(py_version)) {
    return null
      }
      return root.Bokeh.versions.get(py_version);
    } else if (root.Bokeh.version === py_version) {
      return root.Bokeh
    }
    return null
  }
  function is_loaded(root) {
    var Bokeh = get_bokeh(root)
    return (Bokeh != null && Bokeh.Panel !== undefined)
  }
  if (is_loaded(root)) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (is_loaded(root)) {
        clearInterval(timer);
        embed_document(root);
      } else if (document.readyState == "complete") {
        attempts++;
        if (attempts > 200) {
          clearInterval(timer);
      var Bokeh = get_bokeh(root)
      if (Bokeh == null || Bokeh.Panel == null) {
            console.warn("Panel: ERROR: Unable to run Panel code because Bokeh or Panel library is missing");
      } else {
        console.warn("Panel: WARNING: Attempting to render but not all required libraries could be resolved.")
        embed_document(root)
      }
        }
      }
    }, 25, root)
  }
})(window);</script>
:::

::: {.cell-output .cell-output-display}
:::

::: {.cell-output .cell-output-display}
:::

::: {.cell-output .cell-output-display execution_count="31"}
<div id='07b9ae0c-5c57-45f7-9449-de8dcd394f41'>
  <div id="a2e83c71-fd56-45a1-a177-57b8c04fb793" data-root-id="07b9ae0c-5c57-45f7-9449-de8dcd394f41" style="display: contents;"></div>
</div>
<script type="application/javascript">(function(root) {
  var docs_json = {"16f536eb-21ad-411e-9084-70424150b3b3":{"version":"3.5.2","title":"Bokeh Application","roots":[{"type":"object","name":"panel.models.layout.Column","id":"07b9ae0c-5c57-45f7-9449-de8dcd394f41","attributes":{"name":"Column00526","stylesheets":["\n:host(.pn-loading):before, .pn-loading:before {\n  background-color: #c3c3c3;\n  mask-size: auto calc(min(50%, 400px));\n  -webkit-mask-size: auto calc(min(50%, 400px));\n}",{"type":"object","name":"ImportedStyleSheet","id":"a41204fd-5147-47ee-9449-cfb0f2fd0a66","attributes":{"url":"https://cdn.holoviz.org/panel/1.5.4/dist/css/loading.css"}},{"type":"object","name":"ImportedStyleSheet","id":"463262e8-c05b-4209-b12e-259d4f210b63","attributes":{"url":"https://cdn.holoviz.org/panel/1.5.4/dist/css/listpanel.css"}},{"type":"object","name":"ImportedStyleSheet","id":"02483291-d4ae-4ff9-8099-22bb13ab4941","attributes":{"url":"https://cdn.holoviz.org/panel/1.5.4/dist/bundled/theme/default.css"}},{"type":"object","name":"ImportedStyleSheet","id":"7ab8784f-27ef-4ee2-8566-c05caa18b20a","attributes":{"url":"https://cdn.holoviz.org/panel/1.5.4/dist/bundled/theme/native.css"}}],"margin":0,"align":"start","children":[{"type":"object","name":"Figure","id":"a1434212-8bee-4515-85d0-98d8a4590d24","attributes":{"width":null,"height":null,"margin":[5,10],"sizing_mode":"fixed","align":"start","x_range":{"type":"object","name":"Range1d","id":"7efb43de-5f47-4ca3-bd21-e976b9eef3be","attributes":{"name":"x","tags":[[["x",null]],[]],"start":-10719355.744501399,"end":18012496.11327679,"reset_start":-10719355.744501399,"reset_end":18012496.11327679}},"y_range":{"type":"object","name":"Range1d","id":"056fc6c2-e9c7-4077-b3ff-fa9a1db30d06","attributes":{"name":"y","tags":[[["y",null]],{"type":"map","entries":[["invert_yaxis",false],["autorange",false]]}],"start":2043860.942045838,"end":12050427.99463108,"reset_start":2043860.942045838,"reset_end":12050427.99463108}},"x_scale":{"type":"object","name":"LinearScale","id":"8d8f1166-cb0f-4634-b7e1-2e921d546bac"},"y_scale":{"type":"object","name":"LinearScale","id":"0c54056b-07fe-4bcb-a588-f2ae217f4287"},"title":{"type":"object","name":"Title","id":"721aa060-d40d-46a4-abd4-9091afca7555","attributes":{"text":"Antigone canadensis Sandhill Crane Migration","text_color":"black","text_font_size":"12pt"}},"renderers":[{"type":"object","name":"TileRenderer","id":"9d48b7fd-4696-4ce2-9f9c-b8392278addb","attributes":{"level":"glyph","tile_source":{"type":"object","name":"WMTSTileSource","id":"63efd3e6-1d5f-4c61-a125-27923b9f78ea","attributes":{"url":"https://cartodb-basemaps-4.global.ssl.fastly.net/light_all/{Z}/{X}/{Y}.png","attribution":"&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors, &copy; <a href=\"https://cartodb.com/attributions\">CartoDB</a>"}}}},{"type":"object","name":"GlyphRenderer","id":"6a93db1d-414c-4684-8a81-2132897ec19a","attributes":{"data_source":{"type":"object","name":"ColumnDataSource","id":"db3e263b-4e48-4087-b695-a09c748f4ebc","attributes":{"selected":{"type":"object","name":"Selection","id":"38a46450-a552-466f-b184-ae9c3f4e91b5","attributes":{"indices":[],"line_indices":[]}},"selection_policy":{"type":"object","name":"UnionRenderers","id":"3b91a3fe-7ef7-46f4-88bd-cf8ad9e528ec"},"data":{"type":"map","entries":[["xs",[[[{"type":"ndarray","array":{"type":"bytes","data":"b1H7j+1taUFSxL4EZm9pQThXZoUsV2lBJAmQzndKaUHAofvLiR5pQajU88+z+WhBHlqt1I0AaUEGYKm/AfJoQYbfxQdKE2lBEkJVS54yaUH6sN4nrTJpQbOZhP7uJWlByCc8ydU4aUGpTCdTOmFpQavU7+RicGlBTTuX9bJyaUFTrYPPBYtpQfIOkoZAhmlBqzilT4CiaUEo11RZ/s9pQcHYlY/t5mlBHMOFCQruaUH4uDiTWfBpQWr7+tz5DGpBUVxDxhv9aUE2VVUGtARqQe+PdDXFAmpBN7WaADnyaUG2JWRIC/FpQbz5cJlM6WlBf+LTjpLkaUF4+TbJ79JpQbmUU5ZVyWlBEQsHkyayaUHtgSaJQaNpQV7yAk3xrmlBAPgcizOqaUGIRnK04qBpQUT0dOGhn2lBK8eYgL2NaUHVmeGoBotpQUeOlDNCf2lBftMO2qyKaUFzferWuGdpQQoE5dwpTWlBYZA9xTNPaUGvcYTl+FxpQSyZvolTeWlB83VcVUc/aUFkkiKofR9pQVQgK84UBWlB6XSS3zbGaEFRwRwOSr1oQXJ/P/8rn2hBPOmc+0ifaEFcUjGrUG5oQUocz8pxQ2hBSbscgDAvaEH2qHDwMz1oQXhI/0CZSWhBnNVTsRNOaEF5/CjJnjxoQfYkKRftPWhBCmtpPKMUaEHJgX65Ey9oQeMd5jLlCWhBu+EqOh0NaEE4syZzZPRnQSj6NQZG6WdBkAPy8vvbZ0FMf4E/3JtnQb9/LZsldmdBRURdSwsbZ0GbOqNiro1mQbMT2II6tGZBF6rtqz+cZkExWgcTC6JmQWc1xPIb12ZBXYTtBCvpZkG4qiKy+ONmQfxbPzMJBmdBmf6cNaYBZ0GK763tSNhmQcLOQ9Ws8WZBYRQTUxsbZ0FbQ3/MIilnQZ1k41duJWdBvxLnqHgsZ0HfkIB4XTRnQWrIdPJaRWdBNN2A7EpoZ0HPbyMPqH5nQRm67CDymGdBhp5taYDLZ0FmQjob4dNnQRHaAwwJv2dBwDkEZPDYZ0FGDHiT7u9nQbz53xSn4WdBwbVX6evqZ0FMHXU6n/pnQeInuKsNB2hBQgF56k0daEHNlN2deEpoQfCzeui3UWhBWv6/vQVFaEG0BQN+6FJoQWknmV3JWmhBxo4qjZtPaEGM0NFmd3toQTKgbe/mfGhBmQw3HgydaEF/RGst3qNoQQMVdInFtWhBysC54LbqaEH+/0ogCg5pQSZmTZaqIWlBFbmrjcdCaUElGnEoQkFpQW9R+4/tbWlB"},"shape":[120],"dtype":"float64","order":"little"}]]]],["ys",[[[{"type":"ndarray","array":{"type":"bytes","data":"EBEGW3KnUkHqX4G9dopSQboCznKIaFJBtZSXT/sqUkGjSp4Vuz1SQX/e/OdHEVJBGOJvqHUAUkFAxwib3NJRQROOsjwFVlFBwngM1SFSUUHpn6xAYzxRQYEHxmZQOFFBaMCcojgBUUFV0tzErN1QQSZyXO787lBB0PR9UdMfUUFM2dwqIUBRQSiB4nTMS1FBeaq6pghhUUGZjDbHwShRQT2RWfRzKFFBvR5G5+g6UUEfvSOtOShRQXF2eLnQI1FBDFey/0zyUEFijEzM2PFQQVLu1klQ4FBBsSZ9LwfZUEEcbculOPBQQfTxqo8p4FBBs9D98MjuUEH7HFKRlspQQRCYqt4a11BBjhOz4eS1UEEPNguL37lQQSXUAM9IsFBBecWK0iuaUEGQgGnWP6BQQbByrNuxeFBBFn1F5v5sUEHW7OGUrotQQfpdjMBvhFBBUglt20tjUEFoaLajHjBQQbe8IAVCnk9B4L6aIY12T0FWd48Vj35PQehcaRXfrU5BYRzq5rD1TUF0DmkKt9VNQVRoVZcE/k1Bns+dujhdTUF2IKFCHhVNQU7rWMacTU1Bn1Jt80P3TEG8Tlk1PMdMQV93Uw41Ck1Bbqz54sXxTEF+QcGeLEtNQUPHbsgBJk1B0HN3z01DTUEGQqrvLYhNQRwvsL5n0E1B6xrLWAs/TkHgrX/ixmNOQW6bBjUqbk5BAMEaCjKmTkFOHvm7A5VOQTA8UFfOEE9BQv9sNb4vT0EEsH/6GxFPQSFkvuWXNU9B098ky+ieTkEnpwT8YR9PQSTSnoXUQU9BHq+tVdGTT0HmGJOOeK1PQTQUr82NN09BmLqmx2AoT0GYbNR44VpPQeD8JxqMPU9B51kJiHZ7T0H7D1f1I/1PQfCdTfCmCFBBCEMXuxqIT0FNOaisD6xPQYPEls9v+U9B2dotaYAQUEGmsVRbwN9PQXqBktJUClBBW2Slu7TsT0G8cpgL7ClQQQ0v3TjpP1BBgdO2jEQlUEHy3tEAHANQQZ5E0L6yzE9B6KXNif+uT0FZK0hmFtZPQXdM0PPDBVBBIOw5Qbc6UEFeUc4LAidQQfieNIoT0E9BcRtEp+nNT0HANhuH9w5QQf106ZIoXFBB8TuykMWGUEF7gUbspJFQQcHgQMdi4lBBQEiGnJ96UUHzZE9jd+NRQaO4w2k1E1JBfTu2BhtIUkG/zGafap1SQSDC+VBftVJB1Uy/MOKpUkHab6qCOoVSQZxrithvplJBM+dNgHOaUkGriCiMS3xSQRARBltyp1JB"},"shape":[120],"dtype":"float64","order":"little"}]]]],["norm_occurrences",{"type":"ndarray","array":{"type":"bytes","data":"AAAAAAAAyD8="},"shape":[1],"dtype":"float64","order":"little"}],["color",{"type":"ndarray","array":{"type":"bytes","data":"AAAAAAAAyD8="},"shape":[1],"dtype":"float64","order":"little"}]]}}},"view":{"type":"object","name":"CDSView","id":"08058fd1-5818-46f0-bea0-756b1203e4f7","attributes":{"filter":{"type":"object","name":"AllIndices","id":"dd9f7f3e-cb7e-444e-9be0-1b5f26e0a4a7"}}},"glyph":{"type":"object","name":"MultiPolygons","id":"181d8ef1-53f4-4371-ad8c-bee642acf498","attributes":{"xs":{"type":"field","field":"xs"},"ys":{"type":"field","field":"ys"},"fill_color":{"type":"field","field":"color","transform":{"type":"object","name":"LinearColorMapper","id":"5994b26f-9381-4c06-8e69-8a93c3ef43f6","attributes":{"palette":["#b3fef5","#b0fef5","#adfdf5","#a9fcf5","#a6fbf6","#a3faf6","#a0faf6","#9df9f6","#9af8f6","#97f7f6","#93f7f6","#90f6f6","#8df5f6","#8af4f7","#87f3f7","#83f2f7","#80f2f7","#7df1f7","#79f0f7","#76eff7","#73eef7","#6fedf8","#6cecf8","#68ecf8","#65ebf8","#61eaf8","#5ee9f8","#5ae8f8","#57e7f8","#53e6f8","#50e5f9","#4ce4f9","#49e3f9","#45e2f9","#42e1f9","#3ee0f9","#3bdff9","#38def9","#35ddf9","#32dcf9","#30dbfa","#2ed9fa","#2dd8fa","#2cd7fa","#2bd6fa","#2bd5fa","#2ad3fa","#2ad2fa","#29d1fa","#29d0fb","#29cffb","#28cdfb","#28ccfb","#28cbfb","#28cafb","#28c8fb","#28c7fb","#29c6fb","#29c5fb","#29c4fb","#29c2fb","#2ac1fb","#2ac0fb","#2bbffb","#2bbdfc","#2cbcfc","#2dbbfc","#2db9fc","#2eb8fc","#2fb7fc","#2fb6fc","#30b4fc","#31b3fc","#32b2fc","#32b0fc","#33affc","#33aefc","#34adfc","#34abfc","#34aafc","#35a9fc","#35a8fc","#35a6fc","#35a5fc","#35a4fc","#35a3fc","#35a1fc","#35a0fc","#359ffc","#359dfc","#359cfc","#359bfc","#349afd","#3498fd","#3497fd","#3396fd","#3395fd","#3293fd","#3292fd","#3191fd","#3090fd","#308ffd","#2f8dfd","#2f8cfd","#2e8bfd","#2e8afd","#2d88fd","#2d87fd","#2c86fd","#2c84fd","#2c83fd","#2c82fd","#2b81fd","#2b7ffd","#2b7efd","#2b7dfd","#2b7bfd","#2b7afd","#2b79fd","#2b77fd","#2b76fd","#2b75fd","#2b73fd","#2c72fd","#2c71fd","#2c6ffd","#2c6efd","#2d6cfd","#2d6bfd","#2d6afc","#2e68fc","#2e67fc","#2e65fc","#2e64fc","#2f62fc","#2f61fc","#2f5ffc","#2f5efc","#2f5dfc","#2f5bfc","#2f5afc","#2f58fb","#2f57fb","#2f55fb","#2f53fb","#2f52fb","#2f50fb","#2f4ffb","#2f4dfb","#2e4cfb","#2e4afb","#2e48fb","#2e47fa","#2d45fa","#2d43fa","#2d42fa","#2d40fa","#2c3efa","#2c3dfa","#2b3bf9","#2b39f9","#2a37f9","#2a36f8","#2934f8","#2832f7","#2831f7","#272ff6","#262ef5","#252cf5","#252af4","#2429f3","#2327f2","#2226f1","#2124f0","#2023ef","#1f22ee","#1e20ed","#1d1feb","#1c1eea","#1b1ce9","#1a1be7","#181ae6","#1719e5","#1618e3","#1417e1","#1316e0","#1215de","#1014dc","#0f13db","#0e12d9","#0d11d7","#0c10d5","#0b0fd3","#0a0ed1","#090dd0","#080dce","#080ccc","#070bca","#070ac8","#0709c6","#0708c4","#0707c2","#0707bf","#0806bd","#0806bb","#0905b9","#0904b7","#0a04b5","#0a04b2","#0b03b0","#0c03ae","#0d02ab","#0e02a9","#0e02a7","#0f02a4","#0f01a2","#1001a0","#10019d","#10019b","#100199","#100197","#100194","#0f0192","#0f0190","#0f018e","#0e018b","#0e0189","#0d0187","#0d0185","#0c0183","#0b0181","#0b017e","#0a017c","#09017a","#090178","#080276","#070274","#060272","#060270","#05026e","#04026c","#030269","#030267","#020265","#010263","#010261","#00025f","#00025d","#00025b","#000259","#000257","#000255","#000154","#000152","#000150","#00004e"],"low":-0.8125,"high":1.1875}}},"hatch_color":{"type":"field","field":"color","transform":{"id":"5994b26f-9381-4c06-8e69-8a93c3ef43f6"}}}},"selection_glyph":{"type":"object","name":"MultiPolygons","id":"ff029f6d-b20b-445a-b1c6-986437b44ced","attributes":{"xs":{"type":"field","field":"xs"},"ys":{"type":"field","field":"ys"},"fill_color":{"type":"field","field":"color","transform":{"id":"5994b26f-9381-4c06-8e69-8a93c3ef43f6"}},"hatch_color":{"type":"field","field":"color","transform":{"id":"5994b26f-9381-4c06-8e69-8a93c3ef43f6"}}}},"nonselection_glyph":{"type":"object","name":"MultiPolygons","id":"dbfde7ac-b6e4-4bc5-810e-396090f3221b","attributes":{"xs":{"type":"field","field":"xs"},"ys":{"type":"field","field":"ys"},"line_alpha":{"type":"value","value":0.1},"fill_color":{"type":"field","field":"color","transform":{"id":"5994b26f-9381-4c06-8e69-8a93c3ef43f6"}},"fill_alpha":{"type":"value","value":0.1},"hatch_color":{"type":"field","field":"color","transform":{"id":"5994b26f-9381-4c06-8e69-8a93c3ef43f6"}},"hatch_alpha":{"type":"value","value":0.1}}},"hover_glyph":{"type":"object","name":"MultiPolygons","id":"02e733e8-10e4-42ca-8185-dd1009ea15b1","attributes":{"xs":{"type":"field","field":"xs"},"ys":{"type":"field","field":"ys"},"fill_color":{"type":"field","field":"color","transform":{"id":"5994b26f-9381-4c06-8e69-8a93c3ef43f6"}},"hatch_color":{"type":"field","field":"color","transform":{"id":"5994b26f-9381-4c06-8e69-8a93c3ef43f6"}}}},"muted_glyph":{"type":"object","name":"MultiPolygons","id":"eb4663c7-6a4c-4f2e-a453-bae82519ede5","attributes":{"xs":{"type":"field","field":"xs"},"ys":{"type":"field","field":"ys"},"line_alpha":{"type":"value","value":0.2},"fill_color":{"type":"field","field":"color","transform":{"id":"5994b26f-9381-4c06-8e69-8a93c3ef43f6"}},"fill_alpha":{"type":"value","value":0.2},"hatch_color":{"type":"field","field":"color","transform":{"id":"5994b26f-9381-4c06-8e69-8a93c3ef43f6"}},"hatch_alpha":{"type":"value","value":0.2}}}}}],"toolbar":{"type":"object","name":"Toolbar","id":"320953d9-48a0-463f-a745-ac1608059a00","attributes":{"tools":[{"type":"object","name":"WheelZoomTool","id":"5b6c5fc9-809c-4a19-a7d8-1bb4f9c2a985","attributes":{"tags":["hv_created"],"renderers":"auto","zoom_together":"none"}},{"type":"object","name":"HoverTool","id":"d8d1af4c-3cb1-43f0-9b7c-9c5b08e4319b","attributes":{"tags":["hv_created"],"renderers":[{"id":"6a93db1d-414c-4684-8a81-2132897ec19a"}],"tooltips":[["norm_occurrences","@{norm_occurrences}"]]}},{"type":"object","name":"SaveTool","id":"9124a04a-9a1e-4787-887b-256d725da2b3"},{"type":"object","name":"PanTool","id":"6fef38f5-8471-4c94-af84-77bbf05f8001"},{"type":"object","name":"BoxZoomTool","id":"9a2e94de-1a41-40bb-b578-669365117287","attributes":{"overlay":{"type":"object","name":"BoxAnnotation","id":"4e6041cc-0eac-4132-9032-904ebeb85582","attributes":{"syncable":false,"line_color":"black","line_alpha":1.0,"line_width":2,"line_dash":[4,4],"fill_color":"lightgrey","fill_alpha":0.5,"level":"overlay","visible":false,"left":{"type":"number","value":"nan"},"right":{"type":"number","value":"nan"},"top":{"type":"number","value":"nan"},"bottom":{"type":"number","value":"nan"},"left_units":"canvas","right_units":"canvas","top_units":"canvas","bottom_units":"canvas","handles":{"type":"object","name":"BoxInteractionHandles","id":"ade8ad1f-431f-4615-8214-bfc9bd6a2c26","attributes":{"all":{"type":"object","name":"AreaVisuals","id":"3a911bf8-51ea-4f41-a9d6-6b7cd31b0431","attributes":{"fill_color":"white","hover_fill_color":"lightgray"}}}}}}}},{"type":"object","name":"ResetTool","id":"530166cb-9bb6-4061-9834-c5665dd99ec7"}],"active_drag":{"id":"6fef38f5-8471-4c94-af84-77bbf05f8001"}}},"left":[{"type":"object","name":"LinearAxis","id":"dec91a8b-a3a4-45fe-9a8d-b96acbb1c505","attributes":{"ticker":{"type":"object","name":"BasicTicker","id":"15050946-aaa8-4354-b6dc-8fcdc646cc49","attributes":{"mantissas":[1,2,5]}},"formatter":{"type":"object","name":"BasicTickFormatter","id":"ea938226-e10d-4259-8d58-b240dbbb8568"},"axis_label":"y","major_label_policy":{"type":"object","name":"AllLabels","id":"7e4bc811-4911-4fb8-af30-cc52ee7db0dd"}}}],"below":[{"type":"object","name":"LinearAxis","id":"511eabf7-a27b-4d40-8e18-2533a142b939","attributes":{"ticker":{"type":"object","name":"BasicTicker","id":"1677a4ad-0ed3-490d-b34f-873415131bb9","attributes":{"mantissas":[1,2,5]}},"formatter":{"type":"object","name":"BasicTickFormatter","id":"156a1bff-c9f1-472d-a987-37f233a90e1a"},"axis_label":"x","major_label_policy":{"type":"object","name":"AllLabels","id":"6111f764-7b7c-4ded-aaa5-f8e9705453ea"}}}],"center":[{"type":"object","name":"Grid","id":"78215dcc-5e3b-48a3-8b10-e3ad7e89c823","attributes":{"axis":{"id":"511eabf7-a27b-4d40-8e18-2533a142b939"},"grid_line_color":null}},{"type":"object","name":"Grid","id":"98c67ef9-bc80-46f7-acde-4f9ea5b8486c","attributes":{"dimension":1,"axis":{"id":"dec91a8b-a3a4-45fe-9a8d-b96acbb1c505"},"grid_line_color":null}}],"frame_width":1400,"frame_height":600,"min_border_top":10,"min_border_bottom":10,"min_border_left":10,"min_border_right":10,"output_backend":"webgl","hold_render":false}},{"type":"object","name":"panel.models.layout.Column","id":"e16522a8-2ecf-4d4f-acb0-c870e7193fcc","attributes":{"name":"WidgetBox00522","css_classes":["panel-widget-box"],"stylesheets":["\n:host(.pn-loading):before, .pn-loading:before {\n  background-color: #c3c3c3;\n  mask-size: auto calc(min(50%, 400px));\n  -webkit-mask-size: auto calc(min(50%, 400px));\n}",{"id":"a41204fd-5147-47ee-9449-cfb0f2fd0a66"},{"type":"object","name":"ImportedStyleSheet","id":"a8e3cb6f-e4ff-476b-ba3f-28215416d7df","attributes":{"url":"https://cdn.holoviz.org/panel/1.5.4/dist/css/widgetbox.css"}},{"id":"463262e8-c05b-4209-b12e-259d4f210b63"},{"id":"02483291-d4ae-4ff9-8099-22bb13ab4941"},{"id":"7ab8784f-27ef-4ee2-8566-c05caa18b20a"}],"margin":0,"align":["center","end"],"children":[{"type":"object","name":"panel.models.layout.Column","id":"1f09133e-faf4-4100-8148-02be2490cfce","attributes":{"name":"Column00485","stylesheets":["\n:host(.pn-loading):before, .pn-loading:before {\n  background-color: #c3c3c3;\n  mask-size: auto calc(min(50%, 400px));\n  -webkit-mask-size: auto calc(min(50%, 400px));\n}",{"id":"a41204fd-5147-47ee-9449-cfb0f2fd0a66"},{"id":"463262e8-c05b-4209-b12e-259d4f210b63"},{"id":"02483291-d4ae-4ff9-8099-22bb13ab4941"},{"id":"7ab8784f-27ef-4ee2-8566-c05caa18b20a"}],"margin":0,"align":"start","children":[{"type":"object","name":"Div","id":"77f68cc8-7a68-49fb-babe-2cf353b6c6b1","attributes":{"stylesheets":["\n:host(.pn-loading):before, .pn-loading:before {\n  background-color: #c3c3c3;\n  mask-size: auto calc(min(50%, 400px));\n  -webkit-mask-size: auto calc(min(50%, 400px));\n}",{"id":"a41204fd-5147-47ee-9449-cfb0f2fd0a66"},{"id":"02483291-d4ae-4ff9-8099-22bb13ab4941"},{"id":"7ab8784f-27ef-4ee2-8566-c05caa18b20a"}],"margin":[5,0,0,10],"align":"start","text":"year: <b>1915</b>"}},{"type":"object","name":"Slider","id":"2a126c77-0055-4c0e-a9fc-76e181967c61","attributes":{"js_property_callbacks":{"type":"map","entries":[["change:value",[{"type":"object","name":"CustomJS","id":"fc577b3d-1163-44b4-ab52-8ceb44197480","attributes":{"tags":[[13460000208,[null,"value"],[null,null]]],"args":{"type":"map","entries":[["bidirectional",false],["properties",{"type":"map"}],["source",{"id":"2a126c77-0055-4c0e-a9fc-76e181967c61"}],["target",{"id":"77f68cc8-7a68-49fb-babe-2cf353b6c6b1"}]]},"code":"try { \n    var labels = ['year: <b>1915</b>', 'year: <b>1974</b>', 'year: <b>1975</b>', 'year: <b>1977</b>', 'year: <b>1981</b>', 'year: <b>1982</b>', 'year: <b>1983</b>', 'year: <b>1984</b>', 'year: <b>1985</b>', 'year: <b>1986</b>', 'year: <b>1987</b>', 'year: <b>1988</b>', 'year: <b>1989</b>', 'year: <b>1990</b>', 'year: <b>1991</b>', 'year: <b>1992</b>', 'year: <b>1993</b>', 'year: <b>1994</b>', 'year: <b>1995</b>', 'year: <b>1996</b>', 'year: <b>1997</b>', 'year: <b>1998</b>', 'year: <b>1999</b>', 'year: <b>2000</b>', 'year: <b>2001</b>', 'year: <b>2002</b>', 'year: <b>2004</b>', 'year: <b>2005</b>', 'year: <b>2006</b>', 'year: <b>2007</b>', 'year: <b>2008</b>', 'year: <b>2009</b>', 'year: <b>2010</b>', 'year: <b>2011</b>', 'year: <b>2012</b>', 'year: <b>2013</b>', 'year: <b>2014</b>', 'year: <b>2015</b>', 'year: <b>2016</b>', 'year: <b>2017</b>', 'year: <b>2018</b>', 'year: <b>2019</b>', 'year: <b>2020</b>', 'year: <b>2021</b>', 'year: <b>2022</b>', 'year: <b>2023</b>', 'year: <b>2024</b>', 'year: <b>2025</b>']\n    target.text = labels[source.value]\n     } catch(err) { console.log(err) }"}}]]]},"stylesheets":["\n:host(.pn-loading):before, .pn-loading:before {\n  background-color: #c3c3c3;\n  mask-size: auto calc(min(50%, 400px));\n  -webkit-mask-size: auto calc(min(50%, 400px));\n}",{"id":"a41204fd-5147-47ee-9449-cfb0f2fd0a66"},{"id":"02483291-d4ae-4ff9-8099-22bb13ab4941"},{"id":"7ab8784f-27ef-4ee2-8566-c05caa18b20a"}],"margin":[0,10,5,10],"align":"start","show_value":false,"tooltips":false,"start":0,"end":47,"value":0}}]}}]}}]}},{"type":"object","name":"panel.models.comm_manager.CommManager","id":"6ffa2361-02db-44e9-b544-ba2ecd59dce1","attributes":{"plot_id":"07b9ae0c-5c57-45f7-9449-de8dcd394f41","comm_id":"61321d9a8bc34011a9b4d8c953b21ce3","client_comm_id":"7610897fe06145d9840c9830b94075fb"}}],"defs":[{"type":"model","name":"ReactiveHTML1"},{"type":"model","name":"FlexBox1","properties":[{"name":"align_content","kind":"Any","default":"flex-start"},{"name":"align_items","kind":"Any","default":"flex-start"},{"name":"flex_direction","kind":"Any","default":"row"},{"name":"flex_wrap","kind":"Any","default":"wrap"},{"name":"gap","kind":"Any","default":""},{"name":"justify_content","kind":"Any","default":"flex-start"}]},{"type":"model","name":"FloatPanel1","properties":[{"name":"config","kind":"Any","default":{"type":"map"}},{"name":"contained","kind":"Any","default":true},{"name":"position","kind":"Any","default":"right-top"},{"name":"offsetx","kind":"Any","default":null},{"name":"offsety","kind":"Any","default":null},{"name":"theme","kind":"Any","default":"primary"},{"name":"status","kind":"Any","default":"normalized"}]},{"type":"model","name":"GridStack1","properties":[{"name":"mode","kind":"Any","default":"warn"},{"name":"ncols","kind":"Any","default":null},{"name":"nrows","kind":"Any","default":null},{"name":"allow_resize","kind":"Any","default":true},{"name":"allow_drag","kind":"Any","default":true},{"name":"state","kind":"Any","default":[]}]},{"type":"model","name":"drag1","properties":[{"name":"slider_width","kind":"Any","default":5},{"name":"slider_color","kind":"Any","default":"black"},{"name":"value","kind":"Any","default":50}]},{"type":"model","name":"click1","properties":[{"name":"terminal_output","kind":"Any","default":""},{"name":"debug_name","kind":"Any","default":""},{"name":"clears","kind":"Any","default":0}]},{"type":"model","name":"FastWrapper1","properties":[{"name":"object","kind":"Any","default":null},{"name":"style","kind":"Any","default":null}]},{"type":"model","name":"NotificationAreaBase1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0}]},{"type":"model","name":"NotificationArea1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"notifications","kind":"Any","default":[]},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0},{"name":"types","kind":"Any","default":[{"type":"map","entries":[["type","warning"],["background","#ffc107"],["icon",{"type":"map","entries":[["className","fas fa-exclamation-triangle"],["tagName","i"],["color","white"]]}]]},{"type":"map","entries":[["type","info"],["background","#007bff"],["icon",{"type":"map","entries":[["className","fas fa-info-circle"],["tagName","i"],["color","white"]]}]]}]}]},{"type":"model","name":"Notification","properties":[{"name":"background","kind":"Any","default":null},{"name":"duration","kind":"Any","default":3000},{"name":"icon","kind":"Any","default":null},{"name":"message","kind":"Any","default":""},{"name":"notification_type","kind":"Any","default":null},{"name":"_destroyed","kind":"Any","default":false}]},{"type":"model","name":"TemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"BootstrapTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"TemplateEditor1","properties":[{"name":"layout","kind":"Any","default":[]}]},{"type":"model","name":"MaterialTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"ReactiveESM1","properties":[{"name":"esm_constants","kind":"Any","default":{"type":"map"}}]},{"type":"model","name":"JSComponent1","properties":[{"name":"esm_constants","kind":"Any","default":{"type":"map"}}]},{"type":"model","name":"ReactComponent1","properties":[{"name":"esm_constants","kind":"Any","default":{"type":"map"}}]},{"type":"model","name":"AnyWidgetComponent1","properties":[{"name":"esm_constants","kind":"Any","default":{"type":"map"}}]},{"type":"model","name":"request_value1","properties":[{"name":"fill","kind":"Any","default":"none"},{"name":"_synced","kind":"Any","default":null},{"name":"_request_sync","kind":"Any","default":0}]}]}};
  var render_items = [{"docid":"16f536eb-21ad-411e-9084-70424150b3b3","roots":{"07b9ae0c-5c57-45f7-9449-de8dcd394f41":"a2e83c71-fd56-45a1-a177-57b8c04fb793"},"root_ids":["07b9ae0c-5c57-45f7-9449-de8dcd394f41"]}];
  var docs = Object.values(docs_json)
  if (!docs) {
    return
  }
  const py_version = docs[0].version.replace('rc', '-rc.').replace('.dev', '-dev.')
  async function embed_document(root) {
    var Bokeh = get_bokeh(root)
    await Bokeh.embed.embed_items_notebook(docs_json, render_items);
    for (const render_item of render_items) {
      for (const root_id of render_item.root_ids) {
    const id_el = document.getElementById(root_id)
    if (id_el.children.length && id_el.children[0].hasAttribute('data-root-id')) {
      const root_el = id_el.children[0]
      root_el.id = root_el.id + '-rendered'
      for (const child of root_el.children) {
            // Ensure JupyterLab does not capture keyboard shortcuts
            // see: https://jupyterlab.readthedocs.io/en/4.1.x/extension/notebook.html#keyboard-interaction-model
        child.setAttribute('data-lm-suppress-shortcuts', 'true')
      }
    }
      }
    }
  }
  function get_bokeh(root) {
    if (root.Bokeh === undefined) {
      return null
    } else if (root.Bokeh.version !== py_version) {
      if (root.Bokeh.versions === undefined || !root.Bokeh.versions.has(py_version)) {
    return null
      }
      return root.Bokeh.versions.get(py_version);
    } else if (root.Bokeh.version === py_version) {
      return root.Bokeh
    }
    return null
  }
  function is_loaded(root) {
    var Bokeh = get_bokeh(root)
    return (Bokeh != null && Bokeh.Panel !== undefined)
  }
  if (is_loaded(root)) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (is_loaded(root)) {
        clearInterval(timer);
        embed_document(root);
      } else if (document.readyState == "complete") {
        attempts++;
        if (attempts > 200) {
          clearInterval(timer);
      var Bokeh = get_bokeh(root)
      if (Bokeh == null || Bokeh.Panel == null) {
            console.warn("Panel: ERROR: Unable to run Panel code because Bokeh or Panel library is missing");
      } else {
        console.warn("Panel: WARNING: Attempting to render but not all required libraries could be resolved.")
        embed_document(root)
      }
        }
      }
    }, 25, root)
  }
})(window);</script>
:::
::::::::::

::::: {.cell execution_count="20"}
``` {.python .cell-code}
# Save the plot
occurrence_hvplot.save('siberian-crane-years.html', embed=True)
```

::: {.cell-output .cell-output-stdout}
      0%|          | 0/48 [00:00<?, ?it/s]  6%|▋         | 3/48 [00:00<00:01, 23.71it/s] 12%|█▎        | 6/48 [00:00<00:01, 24.47it/s] 19%|█▉        | 9/48 [00:00<00:01, 24.24it/s] 25%|██▌       | 12/48 [00:00<00:01, 24.79it/s] 31%|███▏      | 15/48 [00:00<00:01, 25.00it/s] 38%|███▊      | 18/48 [00:00<00:01, 25.84it/s] 44%|████▍     | 21/48 [00:00<00:01, 26.61it/s] 50%|█████     | 24/48 [00:00<00:00, 27.05it/s] 56%|█████▋    | 27/48 [00:01<00:00, 27.75it/s] 62%|██████▎   | 30/48 [00:01<00:00, 28.10it/s] 69%|██████▉   | 33/48 [00:01<00:00, 28.27it/s] 75%|███████▌  | 36/48 [00:01<00:00, 28.45it/s] 81%|████████▏ | 39/48 [00:01<00:00, 28.39it/s] 88%|████████▊ | 42/48 [00:01<00:00, 28.67it/s] 94%|█████████▍| 45/48 [00:01<00:00, 29.05it/s]                                               
:::

::: {.cell-output .cell-output-stderr}
    WARNING:bokeh.core.validation.check:W-1005 (FIXED_SIZING_MODE): 'fixed' sizing mode requires width and height to be set: figure(id='c2dc61e3-3e46-448f-9cc2-0b2e2fb9f77a', ...)
:::
:::::
