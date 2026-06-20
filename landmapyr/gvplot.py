"""
Plot Functions with GeoViews.

gvplot_gdf_esri: GV plot of asthma data as chloropleth over ESRI
gvplot_chloropleth: Generate a chloropleth with the given color column
gvplot_ndvi_index: Plot NDVI and CDC data
gvplot_resid: Plot model residual
"""
def gvplot_gdf_esri(place_gdf, index='asthma'):
    """
    GV Plot of asthma data as chloropleth.

    Args:
       place_gdf (gdf): combined gdf 
       index (str, optional): index column name
    """
    import geoviews as gv
    from cartopy import crs as ccrs

    tract_cdc_gv = (
        gv.tile_sources.EsriImagery
        * 
        gv.Polygons(
            place_gdf.to_crs(ccrs.Mercator()),
            vdims=[index, 'tract2010'],
            crs=ccrs.Mercator()
        ).opts(color=index, colorbar=True, tools=['hover'])
    ).opts(width=600, height=600, xaxis=None, yaxis=None)

    return tract_cdc_gv

# tract_cdc_gv = gvplot_gdf(place_gdf)

def gvplot_chloropleth(gdf, **opts):
    """
    Generate a chloropleth with the given color column.
    
    Args:
        gdf (gdf): GeoDataFrame
    Returns:
        _ (gv_plot): plot
    """
    import geoviews as gv
    from cartopy import crs as ccrs
    
    return gv.Polygons(
        gdf.to_crs(ccrs.Mercator()),
        crs=ccrs.Mercator()
    ).opts(xaxis=None, yaxis=None, colorbar=True, **opts)
    
# gvplot_chloropleth(gdf)
    
def gvplot_ndvi_index(place_gdf, index='asthma'):
    """
    Plot NDVI and CDC data.

    Args:
        place_gdf (gdf): merged data as gdf
        index (str, optional): index column name
    Returns:
        gvplot
    """
    gvplot_ndvi = (
        gvplot_chloropleth(place_gdf, color=index, cmap='Blues', title=index.title())
        + 
        gvplot_chloropleth(place_gdf, color='edge_density', cmap='Greens', title='Edge Density')
    )
    
    return gvplot_ndvi
    
# gvplot_ndvi_index(place_gdf, ndvi_index_df)

def gvplot_resid(model_df):
    """
    Plot model residual
    
    Args:
        model_df (df): model object
    Returns:
        resid_gv (gv_plot): plot
    """
    # Plot error geographically as a chloropleth
    resid_gv = (
        gvplot_chloropleth(model_df, color='resid', cmap='RdBu', title="Residuals for Asthma")
        .redim.range(resid=(-.3, .3))
        #.opts(frame_width=600, aspect='equal')
    )
    
    return resid_gv

# gvplot_resid(model_df, yvar='asthma')

