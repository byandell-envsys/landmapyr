def search_earthaccess(delta_gdf, dates=("2023-05", "2023-09")):
    """
    Search EarthAccess for granules overlapping with gdf.

    Args:
        delta_gdf (gdf): GeoDataFrame.
        dates (tuple, optional): Inclusive dates. Defaults to ("2023-05", "2023-09").
    Returns:
        results (list): list of metadata for granules
    """
    import earthaccess

    # Log in to earthaccess
    earthaccess.login(persist=True)
    # Search for HLS tiles
    results = earthaccess.search_data(
        short_name="HLSL30",
        cloud_hosted=True,
        bounding_box=tuple(delta_gdf.total_bounds),
        temporal=dates,  # was ("2024-06", "2024-08")
    )
    return results


# results = search_earthaccess(delta_gdf, ("2023-05", "2023-09"))


def get_earthaccess_links(results):
    """
    Get EarthAccess Links.

    Args:
        results (list):

    Returns:
        _type_: _description_
    """
    import re
    import pandas as pd
    import geopandas as gpd
    import earthaccess
    from tqdm.notebook import tqdm
    from shapely.geometry import Polygon

    url_re = re.compile(
        r"\.(?P<tile_id>\w+)\.\d+T\d+\.v\d\.\d\.(?P<band>[A-Za-z0-9]+)\.tif"
    )

    # Loop through each granule
    link_rows = []
    for granule in tqdm(results):
        # Get granule information
        info_dict = granule["umm"]
        datetime = pd.to_datetime(
            info_dict["TemporalExtent"]["RangeDateTime"]["BeginningDateTime"]
        )
        points = info_dict["SpatialExtent"]["HorizontalSpatialDomain"]["Geometry"][
            "GPolygons"
        ][0]["Boundary"]["Points"]
        geometry = Polygon(
            [(point["Longitude"], point["Latitude"]) for point in points]
        )

        # Get URL
        files = earthaccess.open([granule])

        # Build metadata DataFrame
        for file in files:
            match = url_re.search(file.full_name)
            if match is not None:
                link_rows.append(
                    gpd.GeoDataFrame(
                        dict(
                            datetime=[datetime],
                            tile_id=[match.group("tile_id")],
                            band=[match.group("band")],
                            url=[file],
                            geometry=[geometry],
                        ),
                        crs="EPSG:4326",
                    )
                )

    # Concatenate metadata DataFrame
    file_df = pd.concat(link_rows).reset_index(drop=True)
    return file_df


# file_df = get_earthaccess_links(results)
