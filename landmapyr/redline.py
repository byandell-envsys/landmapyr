"""
Redline functions.

redline_gdf: Read redlining GeoDataFrame from Mapping Inequality
redline_mask: Create new gdf for redlining using regionmask
redline_index_gdf: Merge index stats with redlining gdf into one gdf
"""
def redline_gdf(data_dir):
    """
    Read redlining GeoDataFrame from Mapping Inequality.

    Args:
        data_dir (char): Name of data directory
    Returns:
        place_gdf (gdf): GeoDataFrame for place
    """
    import os # Interoperable file paths
    import geopandas as gpd # Work with vector data
    
    # Define info for redlining download
    redlining_url = (
        "https://dsl.richmond.edu/panorama/redlining/static"
        "/mappinginequality.gpkg"
    )
    redlining_dir = os.path.join(data_dir, 'redlining')
    os.makedirs(redlining_dir, exist_ok=True)
    redlining_path = os.path.join(redlining_dir, 'redlining.shp')

    # Only download once
    if not os.path.exists(redlining_path):
      place_gdf = gpd.read_file(redlining_url)
      place_gdf.to_file(redlining_path)

    # Load from file
    place_gdf = gpd.read_file(redlining_path)
    
    return place_gdf

# place_gdf = redline_gdf(data_dir)

# redline_map(data_dir)

def redline_mask(place_gdf, index_da):
    """
    Create new gdf for redlining using regionmask.
    
    Args:
        place_gdf (gdf): gdf for redlined place
        index_da (da): index for place
    Returns:
        redlining_mask (gdf): gdf with `regionmask` applied.
    """
    import regionmask # Convert shapefile to mask

    redlining_mask = regionmask.mask_geopandas(
        # Put gdf in same CRS as raster
        place_gdf.to_crs(index_da.rio.crs),
        # x and y coordinates from raster data x=504 y=447
        index_da.x, index_da.y,
        # The regions do not overlap
        overlap=False,
        # We're not using geographic coordinates
        wrap_lon=False)
    
    return redlining_mask

# redlining_mask = redline_mask(place_gdf, index_da)

def redline_index_gdf(redlining_gdf, index_stats):
    """
    Merge index stats with redlining gdf into one gdf.
        
    Args:
        redlining_gdf (gdf): gdf for redlined place
        index_stats (da): da with zonal stats
    Returns:
        redlining_index_gdf (gdf): gdf with zonal stats
    """
    import pandas as pd

    redlining_index_gdf = redlining_gdf.merge(
        index_stats.set_index('zone'),
        left_index=True, right_index=True)
    
    # Change grade to ordered Categorical for plotting
    redlining_index_gdf.grade = pd.Categorical(
        redlining_index_gdf.grade,
        ordered=True,
        categories=['A', 'B', 'C', 'D'])

    # Drop rows with NA grades
    redlining_index_gdf = redlining_index_gdf.dropna()

    return redlining_index_gdf

# redlining_index_gdf = redline_index_gdf(redlining_gdf, index_stats)
    