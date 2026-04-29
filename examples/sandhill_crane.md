---
jupyter: python3
title: Access locations and times of Sandhill Crane encounters
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
%pip install -q -e ..
```
:::

::: {.cell execution_count="3"}
``` {.python .cell-code}
from landmapy.initial import create_data_dir, robust_code
```
:::

::: {.cell execution_count="4"}
``` {.python .cell-code}
from landmapy.gbif import gbif_credentials, gbif_species_key
from landmapy.gbif import download_gbif, load_gbif, gbif_monthly
from landmapy.gbif import ecoregions, join_ecoregions_monthly
from landmapy.gbif import count_by_ecoregions
from landmapy.gbif import simplify_ecoregions_gdf, join_occurrence
```
:::

**Import packages:** In the imports cell, we've included some packages
that you will need. Add imports for packages that will help you:

-   Work with reproducible file paths
-   Work with tabular data

For now, run `gbif.py`. Soon, incorporate it into `landmapy` package.

:::: {.cell highlight="true" execution_count="5"}
``` {.python .cell-code}
robust_code()
data_dir = create_data_dir('species')
gbif_dir = create_data_dir('species/gbif_sandhill')
gbif_dir
```

::: {.cell-output .cell-output-display execution_count="3"}
    '/Users/brianyandell/earth-analytics/data/species/gbif_sandhill'
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
> `reset_credentials=True` instead of `reset_credentials=False`.

::: {.cell execution_count="6"}
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

:::: {.cell execution_count="7"}
``` {.python .cell-code}
species_name, species_key = gbif_species_key('grus canadensis')
species_name, species_key
```

::: {.cell-output .cell-output-display execution_count="4"}
    ('Antigone canadensis', 2474953)
:::
::::

### Download data from GBIF

:::: {.cell execution_count="8"}
``` {.python .cell-code}
gbif_path = download_gbif(gbif_dir, species_key)
gbif_path
```

::: {.cell-output .cell-output-display execution_count="5"}
    '/Users/brianyandell/earth-analytics/data/species/gbif_sandhill/0012336-260423192947929.zip'
:::
::::

download key is 0020917-241007104925546 GBIF.org (17 October 2024) GBIF
Occurrence Download https://doi.org/10.15468/dl.4d3k48

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

:::: {.cell execution_count="9"}
``` {.python .cell-code}
gbif_df = load_gbif(gbif_path)
gbif_df.head()
```

::: {.cell-output .cell-output-display execution_count="6"}
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

               countryCode   stateProvince   decimalLatitude   decimalLongitude   month   year
  ------------ ------------- --------------- ----------------- ------------------ ------- ------
  gbifID                                                                                  
  4103735033   US            NaN             40.6437           -98.8950           3       2023
  4953718975   US            NaN             31.5633           -109.7160          11      2023
  4135517029   US            NaN             42.3291           -84.2403           5       2023
  4953718976   US            NaN             32.0840           -109.0510          1       2023
  4953718225   US            NaN             32.0840           -109.0510          3       2023

</div>
:::
::::

### Canada Breeding Locations

:::: {.cell execution_count="10"}
``` {.python .cell-code}
ac_CA = gbif_df.loc[gbif_df['countryCode'] == 'CA']
ac_CA.value_counts()
```

::: {.cell-output .cell-output-display execution_count="7"}
    countryCode  stateProvince     decimalLatitude  decimalLongitude  month  year
    CA           Ontario           41.955400        -82.514000        5      2023    395
                                   42.038967        -82.509125        5      2023    217
                 British Columbia  49.100000        -123.185000       1      2023    183
                 Ontario           44.350597        -79.883620        4      2023    168
                 British Columbia  49.100000        -123.185000       12     2023    159
                                                                                    ... 
                 Ontario           43.349340        -80.209730        5      2023      1
                                   43.349964        -80.375656        4      2023      1
                                   43.353832        -79.860730        4      2023      1
                                   43.354767        -81.499330        4      2023      1
                 Yukon Territory   69.596910        -140.185060       6      2023      1
    Name: count, Length: 15708, dtype: int64
:::
::::

### US Breeding Locations

:::: {.cell execution_count="11"}
``` {.python .cell-code}
ac_US = gbif_df.loc[gbif_df['countryCode'] == 'US']
ac_US.value_counts()
```

::: {.cell-output .cell-output-display execution_count="8"}
    countryCode  stateProvince  decimalLatitude  decimalLongitude  month  year
    US           Ohio           41.627710        -83.191890        5      2023    1576
                                41.645070        -83.263720        5      2023     505
                 Wisconsin      43.033360        -89.351380        4      2023     336
                 Arizona        31.561499        -109.720020       1      2023     321
                 Ohio           41.626520        -83.188970        5      2023     312
                                                                                  ... 
                 Michigan       42.253153        -85.857013        8      2023       1
                                42.253130        -85.988390        5      2023       1
                                42.253110        -83.695220        9      2023       1
                                42.253010        -85.302475        3      2023       1
                 Wyoming (WY)   44.610549        -110.220852       7      2023       1
    Name: count, Length: 103892, dtype: int64
:::
::::

## Convert GBIF data to a GeoDataFrame by Month

:::: {.cell execution_count="12"}
``` {.python .cell-code}
monthly_gdf = gbif_monthly(gbif_df)
monthly_gdf
```

::: {.cell-output .cell-output-display execution_count="9"}
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

               year   month   geometry
  ------------ ------ ------- -----------------------------
  gbifID                      
  4103735033   2023   3       POINT (-98.895 40.6437)
  4953718975   2023   11      POINT (-109.716 31.5633)
  4135517029   2023   5       POINT (-84.2403 42.3291)
  4953718976   2023   1       POINT (-109.051 32.084)
  4953718225   2023   3       POINT (-109.051 32.084)
  \...         \...   \...    \...
  4159135015   2023   5       POINT (-82.54347 41.98161)
  4884744706   2023   7       POINT (-86.14826 42.53785)
  4159295666   2023   5       POINT (-80.4592 42.5761)
  4408876179   2023   7       POINT (-151.51888 59.63738)
  4409335777   2023   8       POINT (-151.52234 59.64154)

<p>313542 rows × 3 columns</p>
</div>
:::
::::

### Download and save ecoregion boundaries

Ecoregions represent boundaries formed by biotic and abiotic conditions:
geology, landforms, soils, vegetation, land use, wildlife, climate, and
hydrology.

:::: {.cell execution_count="13"}
``` {.python .cell-code}
ecoregions_gdf = ecoregions(data_dir)
ecoregions_gdf.plot(edgecolor='black', color='skyblue')
```

::: {.cell-output .cell-output-display}
![](sandhill_crane_files/figure-markdown/fig-ecoregions-output-1.png){#fig-ecoregions}
:::
::::

::: {.cell execution_count="14"}
``` {.python .cell-code}
%%bash
find ~/earth-analytics/data/species -name '*.shp'
```
:::

:::: {.cell execution_count="15"}
``` {.python .cell-code}
%store ecoregions_gdf monthly_gdf
```

::: {.cell-output .cell-output-stdout}
    Stored 'ecoregions_gdf' (GeoDataFrame)
    Stored 'monthly_gdf' (GeoDataFrame)
:::
::::

Identify the ecoregion for each observation

:::: {.cell execution_count="16"}
``` {.python .cell-code}
gbif_ecoregion_gdf = join_ecoregions_monthly(ecoregions_gdf, monthly_gdf)
gbif_ecoregion_gdf
```

::: {.cell-output .cell-output-display execution_count="12"}
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

              year   month   name
  ----------- ------ ------- ----------------------------------
  ecoregion                  
  4           2023   8       Ahklun and Kilbuck Upland Tundra
  4           2023   7       Ahklun and Kilbuck Upland Tundra
  4           2023   7       Ahklun and Kilbuck Upland Tundra
  4           2023   7       Ahklun and Kilbuck Upland Tundra
  4           2023   7       Ahklun and Kilbuck Upland Tundra
  \...        \...   \...    \...
  833         2023   4       Northern Rockies conifer forests
  833         2023   5       Northern Rockies conifer forests
  833         2023   5       Northern Rockies conifer forests
  833         2023   6       Northern Rockies conifer forests
  833         2023   5       Northern Rockies conifer forests

<p>307693 rows × 3 columns</p>
</div>
:::
::::

Count the observations in each ecoregion each month

:::: {.cell execution_count="17"}
``` {.python .cell-code}
occurrence_df = count_by_ecoregions(gbif_ecoregion_gdf, 'ecoregion', 'name', 'month')
occurrence_df
```

::: {.cell-output .cell-output-display execution_count="13"}
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
  4           7       5             0.004427
  9           5       3             0.000745
              6       2             0.001061
              8       8             0.004741
              9       13            0.007170
  \...        \...    \...          \...
  833         7       169           0.004581
              8       173           0.004080
              9       131           0.002875
              10      95            0.001874
              11      25            0.000438

<p>788 rows × 2 columns</p>
</div>
:::
::::

:::: {.cell execution_count="18"}
``` {.python .cell-code}
# plot to check distrubions 
occurrence_df.reset_index().plot.scatter(
    x='month', y='norm_occurrences', c='ecoregion',
    logy=True
)
```

::: {.cell-output .cell-output-display}
![](sandhill_crane_files/figure-markdown/fig-occurrence-by-month-output-1.png){#fig-occurrence-by-month}
:::
::::

Create a simplified GeoDataFrame for plot

:::: {.cell execution_count="19"}
``` {.python .cell-code}
ecoregions_gdf = simplify_ecoregions_gdf(ecoregions_gdf)
ecoregions_gdf
```

::: {.cell-output .cell-output-display execution_count="15"}
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

:::: {.cell execution_count="20"}
``` {.python .cell-code}
%store gbif_path
%who
```

::: {.cell-output .cell-output-stdout}
    Stored 'gbif_path' (str)
    ac_CA    ac_US   count_by_ecoregions     create_data_dir     data_dir    download_gbif   ecoregions  ecoregions_gdf  gbif_credentials    
    gbif_df  gbif_dir    gbif_ecoregion_gdf  gbif_monthly    gbif_path   gbif_species_key    join_ecoregions_monthly     join_occurrence     load_gbif   
    monthly_gdf  occurrence_df   ojs_define  robust_code     simplify_ecoregions_gdf     species_key     species_name    
:::
::::

Mapping monthly distribution

:::: {.cell execution_count="21"}
``` {.python .cell-code}
occurrence_gdf = join_occurrence(ecoregions_gdf, occurrence_df)
occurrence_gdf
```

::: {.cell-output .cell-output-display execution_count="17"}
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

                      name                               area        geometry                                             norm_occurrences
  ----------- ------- ---------------------------------- ----------- ---------------------------------------------------- ------------------
  ecoregion   month                                                                                                       
  4           7       Ahklun and Kilbuck Upland Tundra   8.196573    MULTIPOLYGON (((-17930832.005 8046779.358, -17\...   0.004427
  9           5       Alaska-St. Elias Range tundra      28.388010   MULTIPOLYGON (((-16886232.729 9049093.235, -16\...   0.000745
              6       Alaska-St. Elias Range tundra      28.388010   MULTIPOLYGON (((-16886232.729 9049093.235, -16\...   0.001061
              8       Alaska-St. Elias Range tundra      28.388010   MULTIPOLYGON (((-16886232.729 9049093.235, -16\...   0.004741
              9       Alaska-St. Elias Range tundra      28.388010   MULTIPOLYGON (((-16886232.729 9049093.235, -16\...   0.007170
  \...        \...    \...                               \...        \...                                                 \...
  833         7       Northern Rockies conifer forests   35.905513   POLYGON ((-13358313.218 7236575.932, -13331349\...   0.004581
              8       Northern Rockies conifer forests   35.905513   POLYGON ((-13358313.218 7236575.932, -13331349\...   0.004080
              9       Northern Rockies conifer forests   35.905513   POLYGON ((-13358313.218 7236575.932, -13331349\...   0.002875
              10      Northern Rockies conifer forests   35.905513   POLYGON ((-13358313.218 7236575.932, -13331349\...   0.001874
              11      Northern Rockies conifer forests   35.905513   POLYGON ((-13358313.218 7236575.932, -13331349\...   0.000438

<p>788 rows × 4 columns</p>
</div>
:::
::::

:::: {.cell execution_count="22"}
``` {.python .cell-code}
%store occurrence_gdf
```

::: {.cell-output .cell-output-stdout}
    Stored 'occurrence_gdf' (GeoDataFrame)
:::
::::

### Plot monthly distribution

#### Static Plot

:::: {.cell execution_count="23"}
``` {.python .cell-code}
from landmapy.plots import plot_occurrence
plot_occurrence(occurrence_gdf)
```

::: {.cell-output .cell-output-display}
![](sandhill_crane_files/figure-markdown/fig-occurrence-map-months-output-1.png){#fig-occurrence-map-months}
:::
::::

#### Optional Dynamic Plot

::::::::::::: {.cell execution_count="24"}
``` {.python .cell-code}
from landmapy.hv_plots import hvplot_occurrence
occurrence_hvplot = hvplot_occurrence(occurrence_gdf)
# Save the plot
occurrence_hvplot.save('sandhill-crane-migration.html', embed=True)
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
<div id='8f4692fe-c012-4188-94fe-bb614735bbc3'>
  <div id="f2e9f2f1-1366-4714-ac64-5ff9cde86c74" data-root-id="8f4692fe-c012-4188-94fe-bb614735bbc3" style="display: contents;"></div>
</div>
<script type="application/javascript">(function(root) {
  var docs_json = {"206fc7f5-a2f1-4e3d-a214-a347b0d75c86":{"version":"3.5.2","title":"Bokeh Application","roots":[{"type":"object","name":"panel.models.browser.BrowserInfo","id":"8f4692fe-c012-4188-94fe-bb614735bbc3"},{"type":"object","name":"panel.models.comm_manager.CommManager","id":"ecabb7ae-4627-458c-87aa-59425ce7afc2","attributes":{"plot_id":"8f4692fe-c012-4188-94fe-bb614735bbc3","comm_id":"fe5e3392b9b34e41b4710d04a5921085","client_comm_id":"47951e83480f484487784179c4059ed8"}}],"defs":[{"type":"model","name":"ReactiveHTML1"},{"type":"model","name":"FlexBox1","properties":[{"name":"align_content","kind":"Any","default":"flex-start"},{"name":"align_items","kind":"Any","default":"flex-start"},{"name":"flex_direction","kind":"Any","default":"row"},{"name":"flex_wrap","kind":"Any","default":"wrap"},{"name":"gap","kind":"Any","default":""},{"name":"justify_content","kind":"Any","default":"flex-start"}]},{"type":"model","name":"FloatPanel1","properties":[{"name":"config","kind":"Any","default":{"type":"map"}},{"name":"contained","kind":"Any","default":true},{"name":"position","kind":"Any","default":"right-top"},{"name":"offsetx","kind":"Any","default":null},{"name":"offsety","kind":"Any","default":null},{"name":"theme","kind":"Any","default":"primary"},{"name":"status","kind":"Any","default":"normalized"}]},{"type":"model","name":"GridStack1","properties":[{"name":"mode","kind":"Any","default":"warn"},{"name":"ncols","kind":"Any","default":null},{"name":"nrows","kind":"Any","default":null},{"name":"allow_resize","kind":"Any","default":true},{"name":"allow_drag","kind":"Any","default":true},{"name":"state","kind":"Any","default":[]}]},{"type":"model","name":"drag1","properties":[{"name":"slider_width","kind":"Any","default":5},{"name":"slider_color","kind":"Any","default":"black"},{"name":"value","kind":"Any","default":50}]},{"type":"model","name":"click1","properties":[{"name":"terminal_output","kind":"Any","default":""},{"name":"debug_name","kind":"Any","default":""},{"name":"clears","kind":"Any","default":0}]},{"type":"model","name":"FastWrapper1","properties":[{"name":"object","kind":"Any","default":null},{"name":"style","kind":"Any","default":null}]},{"type":"model","name":"NotificationAreaBase1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0}]},{"type":"model","name":"NotificationArea1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"notifications","kind":"Any","default":[]},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0},{"name":"types","kind":"Any","default":[{"type":"map","entries":[["type","warning"],["background","#ffc107"],["icon",{"type":"map","entries":[["className","fas fa-exclamation-triangle"],["tagName","i"],["color","white"]]}]]},{"type":"map","entries":[["type","info"],["background","#007bff"],["icon",{"type":"map","entries":[["className","fas fa-info-circle"],["tagName","i"],["color","white"]]}]]}]}]},{"type":"model","name":"Notification","properties":[{"name":"background","kind":"Any","default":null},{"name":"duration","kind":"Any","default":3000},{"name":"icon","kind":"Any","default":null},{"name":"message","kind":"Any","default":""},{"name":"notification_type","kind":"Any","default":null},{"name":"_destroyed","kind":"Any","default":false}]},{"type":"model","name":"TemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"BootstrapTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"TemplateEditor1","properties":[{"name":"layout","kind":"Any","default":[]}]},{"type":"model","name":"MaterialTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"ReactiveESM1","properties":[{"name":"esm_constants","kind":"Any","default":{"type":"map"}}]},{"type":"model","name":"JSComponent1","properties":[{"name":"esm_constants","kind":"Any","default":{"type":"map"}}]},{"type":"model","name":"ReactComponent1","properties":[{"name":"esm_constants","kind":"Any","default":{"type":"map"}}]},{"type":"model","name":"AnyWidgetComponent1","properties":[{"name":"esm_constants","kind":"Any","default":{"type":"map"}}]},{"type":"model","name":"request_value1","properties":[{"name":"fill","kind":"Any","default":"none"},{"name":"_synced","kind":"Any","default":null},{"name":"_request_sync","kind":"Any","default":0}]}]}};
  var render_items = [{"docid":"206fc7f5-a2f1-4e3d-a214-a347b0d75c86","roots":{"8f4692fe-c012-4188-94fe-bb614735bbc3":"f2e9f2f1-1366-4714-ac64-5ff9cde86c74"},"root_ids":["8f4692fe-c012-4188-94fe-bb614735bbc3"]}];
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

::: {.cell-output .cell-output-stdout}
      0%|          | 0/12 [00:00<?, ?it/s] 17%|█▋        | 2/12 [00:00<00:00, 14.90it/s] 33%|███▎      | 4/12 [00:00<00:00, 12.53it/s] 50%|█████     | 6/12 [00:00<00:00, 11.38it/s] 67%|██████▋   | 8/12 [00:00<00:00, 10.92it/s] 83%|████████▎ | 10/12 [00:00<00:00, 11.61it/s]100%|██████████| 12/12 [00:00<00:00, 12.87it/s]                                               
:::

::: {.cell-output .cell-output-stderr}
    WARNING:W-1005 (FIXED_SIZING_MODE): 'fixed' sizing mode requires width and height to be set: figure(id='c1c290c3-e2d4-4a67-82d6-cd4dc4fffb7e', ...)
:::

::: {.cell-output .cell-output-stdout}
:::
:::::::::::::

``` {.python .cell-code}
occurrence_hvplot
```

#### April Observations

::: {.cell execution_count="26"}
``` {.python .cell-code}
occurrence_gdf_complete = occurrence_gdf.reset_index()

april_occ = occurrence_gdf_complete.loc[occurrence_gdf_complete['month'] == 4].sort_values(by=['norm_occurrences'], ascending=False)

april_occ_top_5 = april_occ[0:5]
april_occ_bottom_5 = april_occ[-5:]
```
:::

:::: {.cell execution_count="27"}
``` {.python .cell-code}
# Top Five Ecoregions

april_occ_top_5
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

        ecoregion   month   name                                       area        geometry                                             norm_occurrences
  ----- ----------- ------- ------------------------------------------ ----------- ---------------------------------------------------- ------------------
  115   81          4       British Columbia coastal conifer forests   14.653986   MULTIPOLYGON (((-14364688.43 7420408.623, -143\...   0.007219
  225   149         4       Central Tallgrass prairie                  36.779324   POLYGON ((-10534926.556 5619565.277, -10517878\...   0.005960
  557   546         4       Palouse prairie                            9.866972    MULTIPOLYGON (((-12951912.056 5827151.995, -12\...   0.005675
  257   173         4       Colorado Rockies forests                   15.113154   MULTIPOLYGON (((-12173003.318 4534115.934, -12\...   0.005394
  487   471         4       New England-Acadian forests                38.509900   MULTIPOLYGON (((-7182650.847 5741141.666, -715\...   0.004976

</div>
:::
::::

:::: {.cell execution_count="28"}
``` {.python .cell-code}
# Bottom Five Ecoregions

april_occ_bottom_5
```

::: {.cell-output .cell-output-display execution_count="23"}
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

        ecoregion   month   name                                    area        geometry                                             norm_occurrences
  ----- ----------- ------- --------------------------------------- ----------- ---------------------------------------------------- ------------------
  611   639         4       Sonoran desert                          21.416224   MULTIPOLYGON (((-12499491.62 3383569.444, -124\...   0.000087
  136   88          4       California coastal sage and chaparral   3.172258    MULTIPOLYGON (((-12820829.454 3243992.707, -12\...   0.000087
  237   162         4       Chihuahuan desert                       46.807295   MULTIPOLYGON (((-12343440.455 3790837.437, -12\...   0.000079
  711   783         4       Western Gulf coastal grasslands         8.340400    POLYGON ((-10826974.582 3185079.852, -10843709\...   0.000029
  127   87          4       California Central Valley grasslands    4.727694    POLYGON ((-13595834.408 4868653.384, -13554815\...   0.000023

</div>
:::
::::
