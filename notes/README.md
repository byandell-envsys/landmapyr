---
title: "EDA Notes for Habitat Suitability"
---

# EDA Notes for Habitat Suitability

These are notes on python techniques accompanying the 2024-25
[Earth Data Analytics](https://github.com/byandell-envsys/EarthDataAnalytics)
course.

### Rest of semester

- 4/10 project pitch & message box
- 4/15 data overview
- 4/17 peer reviews of pitches & message
- 5/1 project presentation
- 5/2 project report & github repo
- 5/6 peer review & presentations

The term ends August 8th.
We’ll have final presentations on the 5th,
and reports due probably the 10th.

### Table of Contents

- [EDA Notes for Habitat Suitability](#eda-notes-for-habitat-suitability)
    - [Rest of semester](#rest-of-semester)
    - [Table of Contents](#table-of-contents)
  - [Notes 3 Apr 2025](#notes-3-apr-2025)
  - [Notes 1 Apr 2025](#notes-1-apr-2025)
    - [Open-source reference manager](#open-source-reference-manager)
    - [References and Such](#references-and-such)
    - [Message Box](#message-box)
  - [Notes 6 Mar 2025](#notes-6-mar-2025)
  - [Notes 4 Mar 2025](#notes-4-mar-2025)
  - [Fuzzy Logic Model 27 Feb 2025](#fuzzy-logic-model-27-feb-2025)
  - [GBIF review 25 Feb 2025](#gbif-review-25-feb-2025)
  - [Classes 20 Feb 2025](#classes-20-feb-2025)

See also `notes_*.md` files
(or their source files `notes_*.qmd`) cited in named sections.
They were rendered for easy viewing in GitHub using the following
[Quarto](https://quarto.org)
commands via the shell:

```bash
quarto render notes_fuzzy.qmd -t markdown
quarto render notes_gbif.qmd -t markdown
quarto render notes_class.qmd -t markdown
```

## Notes 3 Apr 2025

Hannah and Randi project

- [NEON VITALS GitHub](https://github.com/NEONScience/VITALS/tree/main)
- [NASA Earth Surface Mineral Dust Source Investigation (EMIT)](https://earth.jpl.nasa.gov/emit/mission/about)
(first data July 27, 2022)

Yellowstone fire 2022

## Notes 1 Apr 2025

### Open-source reference manager

- [Zotero](https://zotero.org)
- [Mendeley](https://www.mendeley.com/)
- [Wikipedia Comparison](https://en.wikipedia.org/wiki/Comparison_of_reference_management_software)

### References and Such

- [CU Boulder VPN](https://oit.colorado.edu/services/network-internet-services/vpn)
- [Web of Science](https://www.webofscience.com/wos/woscc/basic-search)
- [Google Scholar](https://scholar.google.com/)
- [JSTOR](https://www.jstor.org/)

### [Message Box](https://www.compassscicomm.org/leadership-development/the-message-box/)

[Assignment](https://canvas.colorado.edu/courses/115453/discussion_topics/1535752)

Audience (big picture)
Issue (specific)

- Problems? (what)
- So What? (why)
- Solutions? (how)
- Benefits? (impact)
  
## Notes 6 Mar 2025

Multiple subplots across a page.

Change plot labels. Do outside loop.

```python
plt.xlabel("axis name 1")
plt.ylabel("axis name 2")
```

Change titles of plots

```python
soil_title = [,,,]
# in for loop:
axes[i].set_title(soil_title[i])
```

Line up several soil images across a page.

```python
# Combine the lists
soil_urls = p_soil_url_list + c_soil_url_list

# Set up subplots (adjust rows and columns for layout)
fig, axes = plt.subplots(nrows=1, ncols=len(soil_urls), figsize=(20, 5), constrained_layout=True)

# Loop through each raster, open it, and plot in a subplot
cbar_mappable = None  # To store the QuadMesh object for the colorbar
for i, soil_url in enumerate(soil_urls):
    soil_da = rxr.open_rasterio(soil_url, mask_and_scale=True).squeeze()

    # Plot the raster on the corresponding subplot
    quadmesh = soil_da.plot(ax=axes[i], add_colorbar=False)
    axes[i].set_title(f"Raster {i + 1}")  # Add a title to each subplot

    # Store the QuadMesh object for the colorbar
    if cbar_mappable is None:
        cbar_mappable = quadmesh

# Add a global colorbar
fig.colorbar(cbar_mappable, ax=axes, orientation="horizontal", fraction=0.02, pad=0.1).set_label("Value")

plt.show()
```

## Notes 4 Mar 2025

Data sources

- soil: POLARIS (see cited paper)

```
soil_da = rxr.open_rasterio(
	soil_url,
	mask_and_scale=True
)
```

## Fuzzy Logic Model 27 Feb 2025

You can find it under the "Modules" section on Canvas. Elsa has also provided a link to a conversation with ChatGPTLinks to an external site. that she had on how to implement fuzzy models using scikit-fuzzy in Python, as another resource for you. 

- Elsa demo
  - [Elsa Video on Fuzzy Logic](https://canvas.colorado.edu/courses/115453/modules/items/6282073)
  - [Elsa ChatGPT](https://chatgpt.com/share/67c094af-9724-8000-9004-6f25d266cd85)
  - [notes_fuzzy.md](notes_fuzzy.md) (source [notes_fuzzy.qmd](notes_fuzzy.qmd))
- [Fall 2024 habitatSuitability/4_build](https://github.com/byandell-envsys/habitatSuitability/blob/main/4_build.ipynb)
- [SciKit Fuzzy](https://pypi.org/project/scikit-fuzzy/)
  - [SciKit Fuzzy readthedocs](https://scikit-fuzzy.readthedocs.io/en/latest/)
- [Daniel Kahneman (2011) Thinking Fast and Slow](https://www.middlewaysociety.org/books/psychology-books/thinking-fast-and-slow-by-daniel-kahneman/)

A fuzzy logic model is one that is built on expert knowledge rather than
training data. You may wish to use the
[`scikit-fuzzy`](https://pythonhosted.org/scikit-fuzzy/)
library, which includes many utilities for building this sort of model.
In particular, it contains a number of **membership functions** that
can convert your data into values from 0 to 1 using information such as,
for example, the maximum, minimum, and optimal values for soil pH.

To train a fuzzy logic habitat suitability model:

1. Research S. nutans, and find out what optimal values are for each variable
you are using (e.g. soil pH, slope, and current climatological annual precipitation). 
1. For each **digital number** in each raster, assign a **continuous** value
from 0 to 1 for how close that grid square is to the optimum range
(1=optimal, 0=incompatible). 
1. Combine your layers by multiplying them together.
This will give you a single suitability number for each square.
1. Optionally, you may apply a suitability threshold to make
the most suitable areas pop on your map.

> **Tip**
>
> If you use mathematical operators on a raster in Python, it will
> automatically perform the operation for every number in the raster.
> This type of operation is known as a **vectorized** function. **DO NOT
> DO THIS WITH A LOOP!**. A vectorized function that operates on the
> whole array at once will be much easier and faster.

-   use hill functions to transform harmonized DataArrays into 0-1 DataArrays
-   multiply them together
  
Resources:

- [USDA Natural Resources Convervations Service: Plant Guide: Indiangrass](https://www.nrcs.usda.gov/plantmaterials/etpmcpg13196.pdf)

- [notes_fuzzy.md](notes_fuzzy.md) (source [notes_fuzzy.qmd](notes_fuzzy.qmd))
  - [Brian Notes](notes_fuzzy.md#brian-notes)
  - [Elsa Notes](notes_fuzzy.md#elsa-notes)

## GBIF review 25 Feb 2025

- Katherine Siegel Demo
  - [Katherine Siegel Video](https://canvas.colorado.edu/courses/115453/modules/items/6278820)
  - [notes_gbif.md](notes_gbif.md) (source [notes_gbif.qmd](notes_gbif.qmd))
    - [Brian Notes](notes_gbif.md#brian-notes)
    - [Katherine Notes](notes_gbif.md#katherine-notes)
- https://pygbif.readthedocs.io/en/latest/
- https://github.com/earthlab-education/species-distribution-coding-challenge-byandell/blob/main/notebooks/siberian-crane-species-download.ipynb 
- earthlab-education and look at repos
- [Fall 2024 Species](https://github.com/earthlab-education/species-distribution-coding-challenge-byandell)
  - [gbif.py](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/gbif.py)
  - [sandhill_crane.qmd](https://github.com/earthlab-education/species-distribution-coding-challenge-byandell/blob/main/sandhill_crane.qmd)
  - [siberian_crane.qmd](https://github.com/earthlab-education/species-distribution-coding-challenge-byandell/blob/main/siberian_crane.qmd)

## Classes 20 Feb 2025

- [Katherine Siegel Video on Classes](https://canvas.colorado.edu/courses/115453/modules/items/6273791)
  - [notes_class.md](notes_class.md) (source [notes_class.qmd](notes_class.qmd))
- [EDA Reference for Python Coding: Classes](https://github.com/byandell-envsys/EarthDataAnalytics/blob/main/references.md#classes)
for references and discussion of classes.

A 
[class](https://docs.python.org/3/tutorial/classes.html)
is a function with output of an object that has new methods, which are in turn functions
defined in the class.
In addition, the `@property` decorator defines attributes for the object.
The main use of classes are to:

- add functionality to class
- streamline different functions with same parameters to keep track of metadata
