# Examples Using Landmapy

- [Example EDA Projects Using `landmapy`](#example-eda-projects-using-landmapy)
- [Genesis of `landmapy` Package](#genesis-of-landmapy-package)
- [Technical Notes](#technical-notes)
  - [Python Kernel Selection](#python-kernel-selection)
  - [Python Data Storage](#python-data-storage)
  - [Changes to come](#changes-to-come)

---

## Example EDA Projects Using `landmapy`

To date, this package has been used in the following
[EDA projects](https://github.com/byandell-envsys/EarthDataAnalytics/blob/main/README.md#projects)
(with modules other than
[initial](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/initial.py)
and plot modules):

- [Habitat2: Buffalo Grasslands Habitat Suitability](https://github.com/earthlab-education/habitat-suitability-byandell/blob/main/climate.md)
  - [climate.qmd](climate.qmd)
  - [polaris](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/polaris.py),
[srtm](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/srtm.py),
[thredds](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/thredds.py),
[explore](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/explore.py)
- [Clustering: Classify land cover for Mississippi Delta](https://github.com/earthlab-education/clustering-byandell)
  - [clustering.qmd](clustering.qmd)
  - [reflect](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/reflect.py)
- [Big-Data: Urban Greenspace and Asthma Prevalence](https://github.com/earthlab-education/big-data-byandell/blob/main/big-data.md)
  - [big-data.qmd](big-data.qmd)
  - [naip](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/naip.py),
[explore](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/explore.py)
- [Habitat: Buffalo Grasslands Habitat Suitability](https://github.com/byandell-envsys/habitatSuitability/blob/main/buffalo.md)
  - [buffalo.qmd](buffalo.qmd)
  - [polaris](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/polaris.py),
[srtm](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/srtm.py),
[thredds](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/thredds.py),
[explore](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/explore.py)
- [Redlining: Predicting NDVI for Madison](https://github.com/earthlab-education/fundamentals-04-redlining-byandell/blob/main/notebooks/madison.ipynb)
  - [madison.qmd](madison.qmd)
  - [redline](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/redline.py),
[process](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/process.py),
[explore](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/explore.py)
- [Species: Crane Migration Maps](https://github.com/earthlab-education/species-distribution-coding-challenge-byandell)
  - [sandhill_cranes.qmd](sandhill_cranes.qmd)
  - [siberian_cranes.qmd](siberian_cranes.qmd)
  - [gbif](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/gbif.py)

## Genesis of `landmapy` Package

This `landmapy`python package was begun in nov-dec 2024
when I took the
[Earth Data Analytics (EDA)](https://github.com/byandell-envsys/EarthDataAnalytics)
course as I found
the project tools growing and wanted to find a way
to help me remember and reuse the code I was developing.

EDA staff offered draft code for tools to the class,
which I adapted and expanded, based on their advice.
I learned by doing and looking at other tools,
developing my own
[Coding Strategy](strategy.md).
The Quarto files (`*.qmd`) are rendered as markdown (`*.md`) files
with the shell command

```bash
quarto render [filename].qmd -t markdown
```

with the output files going into the directory
`[filename]_files/figure-markdown/`
as `.png` files.

## Technical Notes

### Python Kernel Selection

The python kernel used for the EDA examples is
`earth-analytics-python`,
which uses Python 3.11.10.
Instructions on installing this kernel via conda can be found at
<https://earthdatascience.org/workshops/setup-earth-analytics-python/setup-python-conda-earth-analytics-environment/>,
which points one to
[Earth Analytics Python Conda Environment](https://github.com/earthlab/earth-analytics-python-env).
If you have this kernel installed,
it is important to ensure that Quarto uses it.
You can set the python kernel by first using a Jupyter notebook.
Alternatively, set the default python kernel for Quarto.
See [Set Default Python Kernel for Quarto](https://github.com/byandell/blob/main/kernel.md)
for more information.

### Python Data Storage

These examples use ephermeral and permanent remote data storage.
See [Documentation on Data Storage](https://github.com/byandell/Documentation/blob/main/python_references.md#data)
for more information.
Some projects use read/write to files, in particular the folder
`~/earth-analytics/data`
is used in the `buffalo.qmd` and the two crane examples.
Note that the location is hardcoded in the python code.
Most projects use python's `Store Magic` class and a shared
`Data` class to provide remote storage and data ingestion.

### Static vs Dynamic Plots

Several of the examples include both static and dynamic plots,
but only static plots are rendered
by default.
Dynamic plots using the `hv_plots` functions
yield much larger plot objects,
which are inherently more flexible.
See [Plot Functions](../plots.md) for more information.

### Changes to come

- Fix `sandhill_cranes.qmd` to get its input saved in python data
- see [render.md](../notes/render.md) for post-rendering that moves images to one folder
`examples/images/[filename]`
- Upload `examples/images/` to the web site
