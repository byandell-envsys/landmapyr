# Translation Prompt from Python to R

**NB:**
_Before proceeding, carefully go over and apply the changes suggested in
[Critique of `transR.md`](transCritic.md)._

**Role:** You are an expert polyglot developer specializing in Python and R (specifically **tidyverse** and **modern base R**). You are an expert in spatial data analysis and manipulation, with particular expertise in **terra**, **stars**, and **sf** for raster and vector spatial data in **R**, and the
[Key Python Spatial Packages in `landmapy](spatial.md)
 for **Python**.
Further, you are an expert in spatial data APIs like those outlined in
[Key APIs and Data Sources in`landmapy`](api.md)
and can make choices of which to use based on the application.

**Task:** Translate the Python code in folder `landmapy` into high-quality, idiomatic R code in new folder `R`.

## Strategy

* **Modularize:** Don't try to translate the whole thing in one go. Translate it **module by module** using the hierarchy outlined in
[Module Hierarchy](hierarchy.md).
* **Flavor:** Use `tidyverse` rather than base R, unless there is a clear performance benefit to using base R.
* **Unit Tests:** After translating the logic, ask the AI to: _"Now, look at the original Python unit tests and write equivalent R tests using the `testthat` package."_

## Requirements

1. **Idiomatic Translation:** Do not perform a literal line-by-line translation. Use R-native structures (e.g., use `purrr::map` instead of explicit `for` loops where appropriate, and use data frames/tibbles for tabular data).
2. **Dependency Mapping:** These include but are not limited to
    * Map `pandas` operations to `dplyr`.
    * Map `numpy` operations to base R vector math or `matrix` operations.
    * Map `matplotlib/seaborn` to `ggplot2`.
    * Map `hvplot` to the R equivalent `hvplot` package.
3. **Functionality:** Ensure the R functions maintain the same input/output logic as the Python originals.
4. **Documentation:** Preserve all docstrings and comments, converting them into **Roxygen2** format (`#'`) for functions.
5. **Error Handling:** Convert Python `try-except` blocks into R `tryCatch()` blocks.

## Constraints

* Use `<-` for assignment, not `=`.
* Explicitly use `package::function()` notation rather than relying on implicit imports.
* Create a `DESCRIPTION` file for the R package that lists all imports in the `Imports` field and suggested uses in the `Suggests` field.
