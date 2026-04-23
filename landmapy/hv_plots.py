"""
Plot Functions with HoloViews.

hvplot_matrix: HV plot of model matrix
hvplot_tract_gdf: HV plot census tracts with satellite imagery background
hvplot_train_test: Plot test fit
hvplot_index_grade: HV plots for index and grade
hvplot_index_pred: Plot the model results
hvplot_delta_gdf: HV Plot Delta GDF
hvplot_cluster: HV Plot of RGB and Clusters
hvplot_occurrence: Holoviews map of monthly occurrences
"""
def hvplot_tract_gdf(place_tract_gdf):
    """
    HV plot census tracts with satellite imagery background.
    
    Args:
        place_tract_gdf (GeoDataFrame): gdf for place
        
    Returns:
        place_hv (hvplot): plot
    """
    from cartopy import crs as ccrs
    
    place_hv = (
        place_tract_gdf
        .to_crs(ccrs.Mercator())
        .hvplot(
            line_color='orange', fill_color=None, 
            crs=ccrs.Mercator(), tiles='EsriImagery',
            frame_width=600)
    )
    return place_hv
    
# hvplot_tract_gdf(place_tract_gdf)

def hvplot_matrix(model_df):
    """
    HV plot of model matrix

    Args:
        model_df (df): model DataFrame
    Returns:
        matrix_hv (hvplot): plot
    """
    import hvplot.pandas
    import hvplot.xarray

    # Plot scatter matrix to identify variables that need transformation
    matrix_hv = hvplot.scatter_matrix(
        model_df
        [[ 
            'mean_patch_size',
            'edge_density',
            'log_asthma'
        ]]
        )
    
    return matrix_hv
    
# hvplot_matrix(ndvi_cdc_gdf)

def hvplot_train_test(y_test, index='asthma'):
    """
    Plot test fit.

    Args:
        y_text (nparray): test dataset
        index (str, optional): index column name
    """
    import holoviews as hv

    # Plot measured vs. predicted index prevalence with a 1-to-1 line
    y_max = y_test[index].max()
    
    hv_test = (
        y_test
        .hvplot.scatter(
            x=index, y=f'pred_{index}',
            xlabel=f'Measured Adult {index.title()} Prevalence', 
            ylabel='fPredicted Adult {index.title()} Prevalence',
            title='Linear Regression Performance - Testing Data'
        )
        .opts(aspect='equal', xlim=(0, y_max), ylim=(0, y_max), height=600, width=600)
    ) * hv.Slope(slope=1, y_intercept=0).opts(color='black')

    return hv_test

# hvplot_train_test(y_test)

def hvplot_index_grade(redlining_index_gdf, place, index='NDVI'):
    """
    HV plots for index and grade.
            
    Args:
        redlining_index_gdf (gdf): gdf with zonal stats
        place (char): Name of selected place
        index (char, optional): index name
    Returns:
        index_hv, grade_hv (hvplot): HV plot objects for mean index and redline grade
    """
    
    index_hv = redlining_index_gdf.hvplot(
        c='mean', geo=True,
        xaxis='Longitude', yaxis='Latitude',
        title = f'{place} Mean {index}',
        clabel=f'Mean {index}', cmap='Greens')
    
    grade_hv = redlining_index_gdf.hvplot(
        c='grade', geo=True,
        xaxis='Longitude', yaxis='Latitude',
        title = place + ' Redlining Grades',
        cmap='cet_diverging_bwr_20_95_c54')

    return index_hv, grade_hv

# index_hv, grade_hv = hvplot_index_grade(redlining_index_gdf)

def hvplot_index_pred(redlining_index_gdf, tree_classifier, place):
    """
    Plot the model results.
            
    Args:
        redlining_index_gdf (gdf): gdf with zonal stats
        tree_classifier (decision_tree): Decision tree for classifier
        place (char): Name of selected place
    Returns:
        pred_hv (hvplot): HV plot object for tree classifier
    """
    
    # Predict grades for each region
    redlining_index_gdf ['predictions'] = (
        tree_classifier.predict(redlining_index_gdf[['mean']]))

    # Subtract actual grades from predicted grades
    redlining_index_gdf['error'] = (
        redlining_index_gdf ['predictions'] - redlining_index_gdf ['grade_codes'])

    # Plot the calculated prediction errors as a chloropleth
    pred_hv = redlining_index_gdf.hvplot(
        c='error', geo=True,
        xaxis='Longitude', yaxis='Latitude',
        clabel='Predicted Grades Error',
        title = place + ' Calculated Prediction Errors')

    return pred_hv

# pred_hv = hvplot_index_pred(redlining_index_gdf, tree_classifier, place)

def hvplot_delta_gdf(delta_gdf, width=600, height=300):
    """
    HV Plot Delta GDF
    
    Args:
        delta_gdf (gdf): area to overlay on topomap
        width (int, optional): width
        height (int, optional): height
    Returns:
        delta_hv (hvplot): HV Plot
    """
    import cartopy.crs as ccrs

    delta_hv = (
        delta_gdf.to_crs(ccrs.Mercator())
        .hvplot(
            alpha=.2, fill_color='white', 
            tiles='EsriImagery', crs=ccrs.Mercator())
        .opts(width=width, height=height)
    )
    return delta_hv

# hvplot_delta_gdf(delta_gdf)

def hvplot_cluster(rgb_sat, model_df):
    """
    HV Plot of RGB and Clusters.
    
    Args:
        rgb_sat (da): rescaled to 0-255 with saturation
        model_df (df): data frame with band data and clusters
    Returns:
        cluster_hv (hvplot): pair of HV plots
    """

    # Plot model_df plus clusters
    # `.sortby()` needed to align spatial relationships.
    
    cluster_hv = (
        rgb_sat.hvplot.rgb( 
            x='x', y='y', bands='band',
            data_aspect=1, # balance aspect ratio
            xaxis=None, yaxis=None)
        + 
        model_df.clusters.to_xarray().sortby(['x', 'y']).hvplot(
            cmap="Colorblind", aspect='equal') 
    )
    return cluster_hv

# hvplot_cluster(reflectance_da)

def hvplot_occurrence(occurrence_gdf, unit='month'):
    """
    Holoviews map of monthly occurrences.

    Args:
        occurrence_gdf (gdf): monthly occurrences of species
        unit (str, optional): 'month' or 'year'
    Returns:
        occurrence_hvplot (hvplot): Holoviews plot of occurrence over time with slider
    """
    import panel as pn
    import calendar
    # CCRS commented out due to bad behavior.
    # import cartopy
    # import cartopy.crs as ccrs

    # Get the plot bounds so they don't change with the slider
    xmin, ymin, xmax, ymax = occurrence_gdf.total_bounds
    
    pn.extension()

    # Define the slider widget
    if unit == 'month':
        options={calendar.month_name[i]: i for i in range(1, 13)}
    else: # 'year'
        options=sorted(
            occurrence_gdf
            .index
            .get_level_values('year')
            .unique()
            .astype(int))
#        {i: i for i in range(1970, 2024)}
    slider = pn.widgets.DiscreteSlider(name=unit, options=options)
    
    occurrence_hvplot = occurrence_gdf.hvplot(
        c='norm_occurrences',
        groupby=unit,
        # Use background tiles
        title='Antigone canadensis Sandhill Crane Migration',
        # geo=True, 
        # crs=ccrs.Mercator(), 
        tiles='CartoLight',
        xlim=(xmin, xmax), ylim=(ymin, ymax),
        frame_height=600,
        frame_width=1400,
        colorbar=False,
        widgets={unit: slider},
        widget_location='bottom',
        width=500,
        height=500
    )
    return occurrence_hvplot

# occurrence_hvplot = hvplot_occurrence(occurrence_gdf)
