# Python Coding Strategy

- [Python Coding Strategy](#python-coding-strategy)
  - [Make Coding Fun](#make-coding-fun)
  - [Build a Function](#build-a-function)
  - [Add Documentation](#add-documentation)
  - [Put a Function in a File](#put-a-function-in-a-file)
  - [Put reusable Module(s) in their own Directory](#put-reusable-modules-in-their-own-directory)
  - [Build a Package from Modules in a Directory](#build-a-package-from-modules-in-a-directory)
  - [Revisit Functions in Modules Often](#revisit-functions-in-modules-often)
  - [Use GitHub as Organizing Tool](#use-github-as-organizing-tool)
  - [Reorganize a Package](#reorganize-a-package)
  - [Import Functions from GitHub](#import-functions-from-github)
  - [Add Further Documentation](#add-further-documentation)
    - [Document Functions in Modules in a Package](#document-functions-in-modules-in-a-package)
  - [Migrate from Jupyter Notebooks to Quarto Documents](#migrate-from-jupyter-notebooks-to-quarto-documents)

## Make Coding Fun

This document has sections entitled with declarative verbs,
in a sense urging me (and you) to follow these directions.
Please take this with a light tone, as I offer suggestions
that have been helpful for me, learned from many teachers over the years.

My approach to coding is organic, intuitive and iterative.
I like to start with a simple, working solution and then build on it.
I find that this approach helps me to better understand the problem
and evolve a simpler, more elegant solution over time.
The goal of my code is to reveal patterns in data
and to make them accessible to others.

[Data evolve](https://byandell.github.io/Data-Evolve/)
over time, and so does code, as my understanding of a project,
and of the patterns in data, grows.
I typically start with something simple.
For instance, when working with envionmental data,
it is often efficient to have a directory (folder) to place data files.
In this course, we started with

```python
import os
import pathlib

data_dir = os.path.join(
    pathlib.Path.home(),
    'earth-analytics',
    'data',
    'habitat'
)
os.makedirs(data_dir, exist_ok=True)
```

## Build a Function

Once I repeatedly use code many times (at least twice),
it is time to create a function that I can reuse.
Note the generalization with a parameter `new_dir`
to allow user to specify a different directory name.

```python
def create_data_dir(new_dir='habitat'):
    import os
    import pathlib

    data_dir = os.path.join(
        pathlib.Path.home(),
        'earth-analytics',
        'data',
        new_dir
    )
    os.makedirs(data_dir, exist_ok=True)

    return data_dir

data_dir = create_data_dir('habitat')
```

## Add Documentation

To remind me of the purpose of the function, I added documentation using
[docstring](https://peps.python.org/pep-0257/).

```python
def create_data_dir(new_dir='habitat'):
    """
    Create Data Directory if it does not exist.

    Args:
        new_dir (char, optional): Name of new directory
    Returns:
        data_dir (char): path to new directory
    """
    import os
    import pathlib

    data_dir = os.path.join(
        pathlib.Path.home(),
        'earth-analytics',
        'data',
        new_dir
    )
    os.makedirs(data_dir, exist_ok=True)

    return data_dir

# data = create_data_dir('habitat')
```

The last comment line is a reminder how to use this function.
Once defined, I follow this suggestion:

```python
data_dir = create_data_dir('habitat')
```

## Put a Function in a File

I then put the function in a (flat) python file,
say using its name `create_data_dir.py`,
which I could import into my notebook or script.

```python
%run create_data_dir.py
```

```python
data_dir = create_data_dir('habitat')
```

The file is re-read from disk with the `%run` magic command,
which is useful for testing the script.
Whenever the file is changed, I need to re-read with `%run`,
with changes to `create_data_dir.py` available immediately.

If the file is in the same folder as my notebook,
I can instead import the function as follows:

```python
from create_data_dir import create_data_dir
data_dir = create_data_dir('habitat')
```

However, to use `import` most effectively requires a few more steps.

## Put reusable Module(s) in their own Directory

The
[references](references.md)
become useful at this point,
particularly
[IPython Interactive Computing](https://ipython.org/ipython-doc/3/interactive/tutorial.html).
When using `import`,
we specifically reload the "module",
as we do with many of the python packages.
Basically a `*.py` file is a module,
and a directory containing `*.py` files is the beginnings of a package
containing multiple modules.
This is academic at this point, but becomes important when working
with larger and/or multiple projects.

Since I plan to use this function in multiple projects,
I will separate it from any particular project by putting it in its own place.
For my purposes, I have projects in folder `~/Documents/GitHub/`,
so I will put the function in a folder `~/Documents/GitHub/landmapyr/`.
For technical reasons (below), I put the function in a subfolder,
also called `landmapyr`.
Further, I expect to have several initializing functions,
so I placed `create_data_director()` in a file
[initial.py](https://github.com/byandell-envsys/landmapyr/blob/main/landmapyr/initial.py).

On my local machine, I have the code for function `create_data_directory()`
in module (file)
`~/Documents/GitHub/landmapyr/landmapyr/initial.py`.
I `%run` the function in this file

```python
%run ~/Documents/GitHub/landmapyr/landmapyr/initial.py
```

and use it as before,

```python
data_dir = create_data_dir('habitat')
```

## Build a Package from Modules in a Directory

Now I have a separate place for code functions used repeatedly,
possibly across multiple projects.
Over time, I create more functions and store them in files in this same place,
`~/Documents/GitHub/landmapyr/landmapyr/`.
While I can `%run` each file as needed as shown above,
it is more efficient to create a package,
which is a directory containing multiple modules.

I chose to call my repo
[landmapyr](https://github.com/byandell-envsys/landmapyr)
because it has python functions for land cover mapping.
(I earlier created a repo called
[landmapr](https://github.com/byandell-envsys/landmapr)
with R code for land cover mapping.)

Again, the
[references](references.md)
become useful at this point, particularly
[Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/).
This shows steps beyond organizing modules in a directory,
to creating a package that can be installed and imported into any project.
We start with the following directory structure:

```
landmapyr/
    landmapyr/
        __init__.py
        initial.py
```

The `__init__.py` is a special file,
which can be empty,
required by python to identify this directory is a package.

```
landmapyr/
    LICENSE         # code license (typically open source)
    README.md       # overview of the package
    pyproject.toml  # or setup.py (there seem to be two ways to do this)
    landmapyr/       # package directory (this is the name the package will be imported as)
        __init__.py # tells python this is a package
        initial.py  # module containing functions
```

I can now import functions from the package as needed after I install the package with 
[pip](https://pypi.org/project/pip/):

```python
#| eval: False
pip install ~/Documents/GitHub/landmapyr
```

The import is slightly different as we access the `initial` module from the `landmapyr` package
and import the function `create_data_dir` from that module.
(The comment line `#| eval: False` is a directive to the markdown interpreter
to not evaluate the following code block.)

```python
from landmapyr.initial import create_data_dir
data_dir = create_data_dir('habitat')
```

## Revisit Functions in Modules Often

I find that I revisit functions in modules often,
to improve them, to add new capabilites, or to reorganize them.
Some of this reorg might involve rethinking a function's
use in different settings.

I also find that I revisit the package structure,
to add new modules, to reorganize modules, or to add new packages.
This might include moving functions among modules,
or creating modules that collect functions of common purpose.
More on that later, I hope.

Once I have created a function, 
I begin to see how I can reuse it in other projects.
I also ponder why I created the function in the first place,
and what might make it more useful in its initial context
and/or in other settings.

How might I improve a function's use?
There are several reasons to revisit a function,
such as changing its

- name to be more descriptive
- parameters to be more general
- return value to be more useful
- internal logic to be more efficient
- documentation to be more informative

It seems best to do this in small steps based on my needs,
rather than imagining a grand plan.
For instance, consider plot functions.
One of the first plots was of a DataArray:

```python
def plot_index(index_da, place, index='NDVI'):
import matplotlib.pyplot as plt # Overlay raster and vector data
#Plot the index_da to see CRS
index_da.plot(
    cbar_kwargs={"label": place},
    robust=True)
plt.gca().set(
    title = f'{place} {index}',
    xlabel='',
    ylabel='')
plt.show()
```

I will probably rename this soon to `plot_da()`,
as it has grown beyond its original usage to plot an NDVI index.
I could imagine more parameters, and make it fancier.
However, for awhile I just moved on.
Later, I wanted to plot multiple DataArrays in a row,
following the idea of another student.
That led to `plot_das()`,
which has options for titles, one or several color bars,
overlay of a GeoDataFrame boundary, and a choice of colormap.
These evolved as I started to use the new function
in multiple settings in the same project.
I realized that another function, `plot_gdf_da()` is now redundant.
You can see these in
[plots.py](https://github.com/byandell-envsys/landmapyr/blob/main/landmapyr/plots.py).

I could eliminate `plot_da()` and `plot_gdf_da()` and use `plot_das()` instead.
However, I would need to go back to earlier projects where I used
them and update the code.
I would also need to update the documentation in the package.
It becomes more complicated if other people depend on the package.
In that case, a "legacy" function might help for awhile, such as:

```python
def plot_da(index_da, place, index='NDVI'):
    """Legacy function: use plot_das()."""
    return plot_das(index_da, titles = f'{place} {index}')
```

## Use GitHub as Organizing Tool

GitHub can be klunky, and at times painful.
However, it provides a place to store functions and modules,
and to organize those into a package.
This `landmapyr` package started as a collection of functions,
then modules, then a package, then a package with documentation.
The history of that is embedded in the GitHub repo
if anyone cares to look.

As I re-imagine a function, or reorg functions in modules,
I can just commit those changes to GitHub knowing that the
earlier versions are still extant, albeit hidden from view.
Further, I can use versioning in the
[pyproject.toml](https://github.com/byandell-envsys/landmapyr/blob/main/pyproject.toml)
file to mark major changes in package reorganization.

## Reorganize a Package

Let's revisit plot functions.
I started with plot functions scattered across modules,
placed there as we developed out projects.
These seemed useful in place, but some had similar purposes,
and I started using them across projects.
At that point, it became helpful to gather them together in one module.

However, I then had plot functions based on different engines,
namely `matplotlib`, `HoloViews` and `GeoViews`,
so I separated these out into different modules.
Since `hv` and `gv` plots are interactive,
they generate large html files that are not easily shared,
and require a server to view.
I began developing `matplotlib` versions that yielded more compact `png` files.
This gave me pause to think about 

I also had plot functions based on different data types,
such as DataArrays, DataFrames, and GeoDataFrames.
This got me thinking about how different types of objects
could be plotted in similar ways.
I have not yet resolved this, but wonder if it would be useful
to have a single function that could plot any of these objects
in a similar way.
That becomes helpful as I make plot functions more versatile,
as in the `plot_das()` function discussed above.
A reason _not_ to generalize is that different plot functions
for different data types have developed different methods
to modify features.
An even more compelling reason is "mission creep",
keeping on task to complete a project rather than build
the all-powerful function.

## Import Functions from GitHub

Building a package adds more machinery,
but it enables me to import a variety of functions
that I maintain on GitHub in a single location, the package
[landmapyr](https://github.com/byandell-envsys/landmapyr).
This package is a repo, just like repos for other projects.

From GitHub, I (and anyone else) can install the package with 
[pip](https://pypi.org/project/pip/):

```python
#| eval: False
pip install git+https://github.com/byandell-envsys/landmapyr.git
```

(Again, comment line `#| eval: False` suppresses markdown evaluation.)
As before, I can import the function as follows:


```python
from landmapyr.initial import create_data_dir
data_dir = create_data_dir('habitat')
```

## Add Further Documentation

Documentation evolves, just as do data, code, and each data-rich project.
My future self, and other users of my code, benefit from documentation
of how functions work, why they are organized in modules,
and what might still be needed to improve a package or project.
The
[References](references.md)
draw on documentation created by the broader community.
This
[Coding Strategy](strategy.md)
page is another form of documentation.
In addition, each project that uses the package can have
its own (compact) documentation referring to the
[landmapyr](https://github.com/byandell-envsys/landmapyr)
and explaining how and why package tools are employed.

### Document Functions in Modules in a Package

Of course, I can add more functions to the package,
but I am mindful that as the package grows,
the need for coherent documentation expands.
I add one-line function calls in
[landmapyr/\_\_init\_\_.py](landmapyr/__init__.py)
and adapt the 
[README.md](README.md)
to describe how to access and use the package,
provide use cases,
and organize modules and functions by topic.
There is a balance of adding documentation and keeping it simple.
My documentation process has evolved to the following approach:

- Add a docstring to each function in a module `*.py`
- Add one-line function descriptions in the top docstring of the module `*.py`
- Add one-line function calls in the `landmapyr/__init__.py` file
- Add one-line module and function information in the `README.md` file

The `landmapyr` package is now large enough that I find it helpful to organize
[Package Modules and Functions](README.md#package-modules-and-functions)
in the
[README.md](README.md)
into (drop-down) blocks around topics:

- Plot Data
- Access Data with APIs
- Explore Data
- Set up Data Mechanics

Readers can then expand the block for a particular module to see the functions contained therein.

## Migrate from Jupyter Notebooks to Quarto Documents

We code in a computing environment,
which includes languages (Python or R and/or
[Julia](https://julialang.org/),
document tools (say Quarto or Jupyter)
and an Integrated Development Environment
([IDE](https://www.codecademy.com/article/what-is-an-ide)),
often
[VS Code](https://code.visualstudio.com/)
or
[Rstudio](https://posit.co/download/rstudio-desktop/).
Most platform tools and many high-level coding documents,
such as Quarto documents, Jupyter notebooks, and
[Rmarkdown](https://rmarkdown.rstudio.com/) documents,
have methods to incorporate code from common languages.

[Quarto](https://quarto.org/) documents are easy to read and use.
To run a Quarto document `*.qmd`, you will need to install
Quarto and some tools (see
[Get Started](https://quarto.org/docs/get-started/)).
Perhaps, see notes in
[my quarto repo](https://github.com/byandell/quarto).

Quarto documents (`*.qmd`) are "flat" markdown files,
an extension of
[Markdown](https://www.markdownguide.org/).
This makes the files small and offers options to render
into common formats including md, html, pdf, and docx.
[Jupyter](https://jupyter.org/) notebooks
(`*.ipynb`) are "nested" json files
that are typically rendered rather than read in raw form.
It is easy to convert between `*.ipynb` and `*.qmd` files
from the shell command line

```bash
quarto convert project.ipynb # convert Jupyter to Quarto
quarto convert project.qmd   # convert Quarto to Jupyter
```

Quarto offers a range of features and project organization tools
that make it easier to read, maintain, edit and share than
Jupyter. This gives the user subsantial flexibility and agency
in how to present material.
It is easy to blend code, text, images and math expressions.
Interactive documents (hosted on a laptop or external server)
can be in a variety of formats, including slide decks.
