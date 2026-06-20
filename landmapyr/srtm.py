"""
SRTM Functions.

srtm_download: Download SRTM data and create DataArray
srtm_slope: Calculate slope from SRTM data
"""


def srtm_download(place_gdf, elevation_dir, buffer=0.1):
    """
    Download SRTM data and create DataArray.

    Parameters
    ----------
    place_gdf: GeoDataFrame
      GeoDataFrame for redlined city
    elevation_dir: character string
      Name of directory with elevation data
    buffer: number
      Buffer around bounds of place_gdf
    Results
    -------
    srtm_da: DataArray
      DataArray of SRTM stuff
    """
    import os
    import earthaccess
    from glob import glob
    import rioxarray as rxr
    import rioxarray.merge as rxrmerge
    from landmapyr.process import clip_gdf_da_bounds

    # Get bounds from gdf.
    bounds = place_gdf.total_bounds
    bounds = bounds + [x * buffer for x in [-1, -1, 1, 1]]  # buffer around place_gdf
    bounds = tuple(bounds)

    # This gets list of granules. Only need to do once.
    srtm_pattern = os.path.join(elevation_dir, "*.hgt.zip")
    if not glob(srtm_pattern):
        earthaccess.login()
        srtm_results = earthaccess.search_data(
            short_name="SRTMGL1", bounding_box=bounds
        )
        srtm_results = earthaccess.download(srtm_results, elevation_dir)

    srtm_da_list = []
    for srtm_path in glob(srtm_pattern):
        tile_da = rxr.open_rasterio(srtm_path, mask_and_scale=True).squeeze()
        tile_da = tile_da.rio.clip_box(*bounds)
        srtm_da_list.append(tile_da)

    srtm_da = rxrmerge.merge_arrays(srtm_da_list)
    # Make sure we are bounding properly.
    srtm_da = clip_gdf_da_bounds(place_gdf, srtm_da, 0.1)

    return srtm_da


# srtm_da = srtm_download(place_gdf, elevation_dir, 0.1)
# srtm_da.plot(cmap='terrain')


def srtm_slope(srtm_da, UTM=32613):
    """
    Calculate slope from SRTM data.

    Project to UTM to calculate slope, then project back.

    Args:
        srtm_da (da): da with elevation information
        UTM (int or char): UTM value (default is for UTM13N)
    Returns:
        slope_da (da): da with slopes (may be slightly different shape from srtm_da)
    """
    import xrspatial

    orig_crs = srtm_da.rio.crs
    srtm_utm_da = srtm_da.rio.reproject(UTM)
    slope_da = xrspatial.slope(srtm_utm_da).rio.reproject(orig_crs)

    return slope_da


# slope_da = srtm_slope(srtm_da, 32613)
