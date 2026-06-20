"""
Process functions.

process_image: Load, crop, and scale a raster image from earthaccess
process_cloud_mask: Load an 8-bit Fmask file and create a boolean mask
process_metadata: Create df of raster data URIs from earthaccess metadata
process_bands: Process bands from gdf with df metadata
clip_gdf_da_bounds: Clip bounds from place_gdf on da extended by buffer (internal)
da2gdf: Convert a DataArray to a GeoDataFrame using rioxarray and geopandas
da_combine: Create 3-D DA combining two 2-D DAs, with optional contrast
"""
def process_image(uri, bounds_gdf):
    """
    Load, crop, and scale a raster image from earthaccess.

    Args:
        uri (file-like or path-like): File accessor downloaded or obtained from earthaccess
        bounds_gdf (gdf): Area of interest to crop to
    Returns:
        cropped_da (da): Processed raster
    """
    import rioxarray as rxr # Work with raster data

    # Connect to the raster image
    da = rxr.open_rasterio(uri, mask_and_scale=True).squeeze()

    # Get the study bounds
    bounds = (
        bounds_gdf
        .to_crs(da.rio.crs)
        .total_bounds
    )
    
    # Crop
    cropped_da = da.rio.clip_box(*bounds)

    return cropped_da

# process_image(city_files[8], city_gdf).plot()

def process_cloud_mask(cloud_uri, bounds_gdf, bits_to_mask):
    """
    Load an 8-bit Fmask file and create a boolean mask.

    Args:
        uri (file-like or path-like): Fmask file accessor downloaded or obtained from earthaccess
        bounds_gdf (gdf): Area of interest to crop to
        bits_to_mask (list of int): The indices of the bits to mask if set
    Returns:
        cloud_mask (array of int): Cloud mask array of bits
    """
    import numpy as np # Process bit-wise cloud mask

    # Open fmask file
    fmask_da = process_image(cloud_uri, bounds_gdf)

    # Unpack the cloud mask bits
    cloud_bits = (
        np.unpackbits(
            (
                # Get the cloud mask as an array...
                fmask_da.values
                # ... of 8-bit integers
                .astype('uint8')
                # With an extra axis to unpack the bits into
                [:, :, np.newaxis]
            ), 
            # List the least significant bit first to match the user guide
            bitorder='little',
            # Expand the array in a new dimension
            axis=-1)
    )

    cloud_mask = np.sum(
        # Select bits
        cloud_bits[:,:,bits_to_mask], 
        # Sum along the bit axis
        axis=-1
    # Check if any of bits are true
    ) == 0
    
    return cloud_mask

# blue_da = process_image(city_files[1], city_redlining_gdf)
# city_cloud_mask = process_cloud_mask(
#     city_files[-1],
#     city_redlining_gdf,
#     [1, 2, 3, 5])
# blue_da.where(city_cloud_mask).plot()

def process_metadata(city_files):
    """
    Create df of raster data URIs from earthaccess metadata.

    Args:
        city_files (file-like URI): File names from earthaccess
    Returns:
        raster_df (df): DataFrame with the metadata
    """
    import re # Use regular expressions to extract metadata
    import pandas as pd # Group and aggregate

    # Compile a regular expression to search for metadata
    uri_re = re.compile(
        r"HLS\.L30\."
        r"(?P<tile_id>T[0-9A-Z]+)\."  # `tile_id`
        r"(?P<date>\d+)T\d+\.v2\.0\." # `date` as `yyyyjjj` (year and Julian date)
        r"(?P<band_id>.+)\.tif")      # `band_id`
    # Find all the metadata in the file name
    uri_groups = [
        uri_re.search(city_file.full_name).groupdict()
        for city_file in city_files]

    # Create a DataFrame with the metadata
    raster_df = pd.DataFrame(uri_groups)

    # Add the File-like URI to the DataFrame
    raster_df['file'] = city_files

    return raster_df

# raster_df = process_metadata(city_files)
# raster_df.head()

def process_bands(city_gdf, raster_df):
    """
    Process bands from gdf with df metadata.

    Args:
        city_gdf (gdf): GeoDataFrame for a city
        raster_df (df): DataFrame of city metadata
    Returns:
        city_das (da): DataArray with image data
    """
    from rioxarray.merge import merge_arrays # Merge rasters

    # Labels for each band to process
    bands = {
        'B02': 'red',
        'B03': 'green',
        'B04': 'blue',
        'B05': 'nir'
    }
    # Initialize structure for saving images
    city_das = {band_name: [] for band_name in bands.values()}
    print('Loading...')
    for tile_id, tile_df in raster_df.groupby('tile_id'):
        print(tile_id)
        # Load the cloud mask
        fmask_file = tile_df[tile_df.band_id=='Fmask'].file.values[0]
        cloud_mask = process_cloud_mask(
            fmask_file, 
            city_gdf, 
            [1, 2, 3, 5])

        for band_id, row in tile_df.groupby('band_id'):
            if band_id in bands:
                band_name = bands[band_id]
                print(band_id, band_name)
                # Process band
                band_da = process_image(
                    row.file.values[0], 
                    city_gdf)

                # Mask band
                band_masked_da = band_da.where(cloud_mask)

                # Store the resulting DataArray for later
                city_das[band_name].append(band_masked_da)

    print('Done.')

    # Merge all tiles
    city_merged_das = {
        band_name: merge_arrays(das) 
        for band_name, das 
        in city_das.items()}

    return city_merged_das

# city_merged_das = process_bands(city_redlining_gdf, raster_df)
# city_merged_das['green'].plot(cmap='Greens', robust=True)

def clip_gdf_da_bounds(place_gdf, da, buffer = 0.1):
    """
    Clip bounds from place_gdf on da extended by buffer.

    The buffer value could be 0.025 instead of 0.1
    
    Args:
        place_gdf (gdf): gdf of selected location
        da (da): da from calling routine
        buffer (float): Buffer around bounds of place_gdf
    Results:
        da (da): da with restricted to bounds of place_gdf 
    """
    bounds = place_gdf.to_crs(da.rio.crs).total_bounds
    bounds = bounds + [x * buffer for x in [-1,-1,1,1]] # buffer around place_gdf
    da = da.rio.clip_box(*bounds)

    return da

# da = clip_gdf_da_bounds(place_gdf, da, 0.1)

def da2gdf(data_array):
    """
    Convert a DataArray to a GeoDataFrame using rioxarray and geopandas.
    
    Args:
        data_array (da): data array
    Returns
        gdf (gdf): GeoDataFrame
    """
    import geopandas as gpd
    from rasterio.features import shapes

    # Ensure the DataArray has spatial information.
    data_array = data_array.rio.write_crs("EPSG:4326")

    # Vectorize DataArray.
    # Mask the DataArray to get only the valid data
    mask = data_array.notnull()

    # Use shapes to convert the DataArray to GeoJSON-like features.
    shapes_gen = shapes(data_array.values, mask=mask.values, transform=data_array.rio.transform())

    # Convert shapes to a GeoDataFrame
    geoms = list(shapes_gen)
    gdf = gpd.GeoDataFrame.from_features([{'geometry': geom, 'properties': {'value': value}} for geom, value in geoms])
    # Set the CRS for the GeoDataFrame:

    gdf.set_crs(data_array.rio.crs, inplace=True)

    return gdf

# gdf = da2gdf(data_array)

def da_combine(da1, da2, titles = ["RCP45","RCP85"], new_dim='rcp', contrast=True):
    """
    Create new DA combining two DAs, with optional contrast.
    
    Args:
        da1, da2 (da): DataArrays to contrast
        titles (list of str): Titles to use as new dimension values.
    Returns:
        da (da): New DataArray with added dimension.
    """
    import xarray as xr
    
    if contrast:
        da = xr.concat([da1, (da1 - da2), da2], dim = new_dim)
        da = da.assign_coords(rcp=[titles[0],'diff',titles[1]])
    else:
        da = xr.concat([da1, da2], dim = new_dim)
        da = da.assign_coords(rcp=titles)
    return da

# da = da_combine(da1, da2)

def merge_da_df(das, value = 'precip', new_dim = 'era', quiet=False):
    """
    Merge DataArrays into a DataFrame.

    Args:
        das (dict): Dictionary of DataArrays
        value (str, optional): Column name for DataArray values. Defaults to 'precip'.
        new_dim (str, optional): Column name for levels of `das`. Defaults to 'era'.
        quiet (bool, optional): Suppress print statements. Defaults to False.

    Returns:
        df (df): DataFrame with DataArray values and new dimensions.
    """
    import pandas as pd

    titles = list(das.keys())
    df = []
    for i in titles:
        if not quiet:
            print(i)
        # Convert DataArray to DataFrame.
        blah = das[i].to_dataframe(name = i).reset_index()
        # Drop NaN values.
        blah = blah.dropna()
        # Only select x (lat), y (lon) and value columns.
        cols = list(blah.columns[[0,1]])
        cols.append(i)
        blah = blah[cols]
        df.append(blah)
        
    # Merge all DataFrames on 'x' and 'y' columns
    merged_df = df[0]
    for dfi in df[1:]:
        merged_df = pd.merge(merged_df, dfi, on=cols[:2])

    return merged_df

# df = merge_da_df(das)