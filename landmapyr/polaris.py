"""
Polaris Functions.

soil_url_dict: Set up soil URLs based on place
merge_soil: Merge soil data
"""


def soil_url_dict(place_gdf, soil_var="sand", soil_sum="mean", soil_depth="100_200"):
    """
    Set up soil URLs based on place.

    Args:
        place_gdf (gdf): gdf of selected location
        soil_var, soil_sum, soil_depth (char): Names of soil variable, summary and depth
    Results:
        soil_url (dict): Dictionary of URLs
    """
    from math import floor, ceil

    soil_url_template = (
        "http://hydrology.cee.duke.edu/POLARIS/PROPERTIES/v1.0/"
        f"{soil_var}/"
        f"{soil_sum}/"
        f"{soil_depth}/"
        "lat{min_lat}{max_lat}_lon{min_lon}{max_lon}.tif"
    )

    # soil_url_template.format(min_lat = 43, max_lat = 44, min_lon = -103, max_lon = -104)

    bounds_min_lon, bounds_min_lat, bounds_max_lon, bounds_max_lat = (
        place_gdf.total_bounds
    )

    # Initialize structure for saving image links
    url_names = []
    for min_lon in range(floor(bounds_min_lon), ceil(bounds_max_lon)):
        for min_lat in range(floor(bounds_min_lat), ceil(bounds_max_lat)):
            url_names.append(f"lon{min_lon}lat{min_lat}")

    soil_urls = {url_name: [] for url_name in url_names}
    for min_lon in range(floor(bounds_min_lon), ceil(bounds_max_lon)):
        for min_lat in range(floor(bounds_min_lat), ceil(bounds_max_lat)):
            print(min_lon, min_lat)
            soil_url = soil_url_template.format(
                min_lat=min_lat,
                max_lat=min_lat + 1,
                min_lon=min_lon,
                max_lon=min_lon + 1,
            )
            soil_urls[f"lon{min_lon}lat{min_lat}"].append(soil_url)

    return soil_urls


# soil_urls = soil_url_dict(place_gdf, "sand", "mean", "100-200")


def merge_soil(
    place_gdf, soil_var="sand", soil_sum="mean", soil_depth="100_200", buffer=0.1
):
    """
    Merge soil data.

    Args:
        place_gdf (gdf): gdf of selected location
        soil_var, soil_sum, soil_depth (char): Names of soil variable, summary and depth
        buffer (float): Buffer around bounds of place_gdf
    Results:
        soil_merged_das (da): soil estimates clipped to bounds of place_gdf
    """
    import rioxarray as rxr
    from rioxarray.merge import merge_arrays  # Merge rasters
    from landmapyr.process import clip_gdf_da_bounds

    soil_urls = soil_url_dict(place_gdf, soil_var, soil_sum, soil_depth)

    # soil_das = {url_name: [] for url_name in list(soil_urls.keys())}
    soil_das = []
    for soil_key in list(soil_urls.keys()):
        soil_url = soil_urls[soil_key][0]
        print(soil_key)
        soil_da = rxr.open_rasterio(soil_url, mask_and_scale=True).squeeze()

        # Store the resulting DataArray for later
        soil_das.append(soil_da)

    print("Done.")

    # Merge all tiles
    soil_merged_das = merge_arrays(soil_das)

    # Use bounds from place_gdf extended by buffer
    # bounds = place_gdf.to_crs(soil_merged_das.rio.crs).total_bounds
    # bounds = bounds + [x * buffer for x in [-1,-1,1,1]] # buffer around place_gdf
    # print(bounds)
    # soil_merged_das = soil_merged_das.rio.clip_box(*bounds)
    soil_merged_das = clip_gdf_da_bounds(place_gdf, soil_merged_das, buffer)

    return soil_merged_das


# soil_merged_das = merge_soil(place_gdf, "sand", "mean", "100_200", 0.1)
