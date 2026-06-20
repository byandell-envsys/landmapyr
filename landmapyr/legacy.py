"""
Legacy Compatibility Layer for landmapyr

This module provides tools to maintain backward compatibility with legacy code
(e.g., from the EarthDataAnalytics course) by aliasing old function names to
their newly refactored counterparts while emitting a DeprecationWarning.

A CSV file mapping is insufficient for Python runtime compatibility without
brittle dynamic code execution. This explicit aliasing is the standard Python approach.
"""

import warnings
import functools
from typing import Callable, Any


def create_deprecated_alias(
    old_name: str, new_func: Callable[..., Any]
) -> Callable[..., Any]:
    """
    Creates a deprecated alias for a refactored function.

    Args:
        old_name (str): The legacy name of the function.
        new_func (Callable): The new function to be called.

    Returns:
        Callable: A wrapped function that emits a DeprecationWarning and calls new_func.
    """

    @functools.wraps(new_func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        warnings.warn(
            f"Call to deprecated function '{old_name}'. "
            f"Please use '{new_func.__module__}.{new_func.__name__}' instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return new_func(*args, **kwargs)

    wrapper.__name__ = old_name
    wrapper.__doc__ = (
        f"Deprecated alias for :func:`{new_func.__module__}.{new_func.__name__}`."
    )
    return wrapper


# ==============================================================================
# Legacy Aliases Definition
# ==============================================================================
# Define legacy aliases below. These should be imported into `landmapyr/__init__.py`
# so that they are exposed at the package level for legacy code.
#
# Example:
# from landmapyr.usgs import get_usgs_data
# old_get_usgs_data = create_deprecated_alias('old_get_usgs_data', get_usgs_data)
