# Walkthrough - Renamed `[oldrepo]` to `[newrepo]`

## Prompt

The repo name has changed from `[oldrepo]` to `[newrepo]`. Go through the rep and update every reference as appropriate. Note that this repo includes a python package currently in the `[oldrepo]` folder, which needs to be moved.

## Changes Made

We have successfully renamed the Python package, directory, and repository references from `[oldrepo]` to `[newrepo]` across the entire codebase.

### 1. Renamed Package Directory

- Moved [oldrepo]` folder to [newrepo] using `git mv`.

### 2. Configuration & Metadata Updates

- Updated [pyproject.toml](pyproject.toml) package specification, homepage, and issues URLs.

### 3. Updated Python Package Code

- Updated package docstring in `[newrepo]/__init__.py`.
- Renamed internal absolute imports of `[oldrepo]/<module>` to `[newrepo].<module>` inside package modules `[newrepo]/*.py`.
- Updated `*.py` imports and test patterns.
- Updated validation in `../tests/verify_qmd_logic.py`.

### 4. Jupyter Notebook Updates

- Updated all occurrences of `[oldrepo]` to `[newrepo]` inside:
  - [package.ipynb](../package.ipynb)
  - [usgs_white_river.ipynb](../scripts/usgs_white_river.ipynb)

### 5. Documentation & Markdown Updates

- Replaced references in 31 markdown (`.md`) and Quarto (`.qmd`) files, including [README.md](file:///Users/brianyandell/Documents/GitHub/landmapyr/README.md), [strategy.md](file:///Users/brianyandell/Documents/GitHub/landmapyr/strategy.md), and [earthpy.qmd](file:///Users/brianyandell/Documents/GitHub/landmapyr/earthpy.qmd).

---

## Verification Results

### Pytest Execution

All tests passed successfully:

```
tests/test_lookup.py .                                                   [ 50%]
tests/test_metadata.py .                                                 [100%]
======================== 2 passed, 2 warnings in 7.47s =========================
```

### Manual Logic Verification

The validation script successfully imports and retrieves USGS site data using the new package name:

```
Searching for: White River near Oglala in SD
Found: WHITE RIVER NEAR OGLALA, SD (06446000)
Fetching metadata for: 06446000
Parameters: ['00060', '00065']
Dates: 1943-06-01 to 2026-06-18
Success: Dynamic metadata retrieval works.
```

## Manual Steps for User

Change [remote "origin"] url in .git/config to point to correct repo.
