# PyPI Packaging and Upload Notes

This document summarizes the steps taken to prepare the `landmapyr` package for its first release on PyPI.

## 1. Package Configuration (`pyproject.toml`)

- **Standard Metadata**: Ensured all project metadata (`description`, `authors`, `readme`, `license`) is located under the `[project]` table per PEP 621.
- **License Formatting**:
  - Used `license = {text = "MIT"}` for modern compatibility.
  - Note: For `setuptools >= 77.0.0`, a simple string like `license = "MIT"` is also supported as an SPDX expression.
- **License Files**: Removed the explicit `license-files` entry. `setuptools` automatically discovers and includes files named `LICENSE` in the distribution.
- **Project URLs**: Added `Homepage` and `Issues` links for better visibility on PyPI.

## 2. Build Environment Setup

- **Tooling**: Installed `build` and `twine` in the environment.
- **The `build/` Conflict**: Discovered that a local directory named `build/` in the repository root causes `python -m build` to fail (as it tries to execute the local folder instead of the library).
  - **Fix**: Always delete `build/` and `landmapyr.egg-info/` before running a fresh build.
- **Command**: Run `python -m build` from the repository root to generate `.tar.gz` and `.whl` files in the `dist/` directory.

## 3. Uploading to PyPI

- **Tools**: Use `twine` for secure uploads.
- **Authentication**:
  - **Username**: Always use `__token__` when using an API token.
  - **Password**: Use the full API token string starting with `pypi-`.
- **First-Time Upload Requirements**:
  - **Email Verification**: Your PyPI account email must be verified before any uploads are allowed.
  - **Token Scope**: For a brand new project, the API token **must** be created with the **"Entire account"** scope. Project-specific tokens only work for projects that already exist on your account.
- **Upload Command**:

    ```bash
    python -m twine upload dist/*
    ```

    *Use `--verbose` to debug 403 Forbidden or authentication errors.*

## 4. Troubleshooting 403 Forbidden

If an upload fails with `403 Forbidden`:

1. Verify the project name (e.g., `landmapyr`) isn't already taken by someone else on PyPI.
2. Ensure your email is verified.
3. Check the API token scope is set to "Entire account".
4. Ensure you are using `__token__` as the username.

## References

- [Tutorial: Packaging a Python Project](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
