"""
Plot Functions with matplotlib.pyplot.

plot_index: Plot index DataArray
plot_gdf_da: Overlay gdf on da map
plot_gdf_state: Plot overlay of redlining GeoDataFrame with state boundaries
plot_gdfs_map: Create Row of Plots
plot_das: Create rows of plots for a list of DataArrays
plot_matrix: Plot of model matrix
plot_train_test: Plot test fit
plot_delta_gdf: Plot Delta GDF
plot_cluster: Plot of RGB and Clusters
""" 
def plot_index(index_da, place, index='NDVI'):
    """
    Plot index DataArray.

    Args:
        index_da (da): index for place
        place (char): Name of selected place
        index (char, optional): index type
    """
    import matplotlib.pyplot as plt # Overlay raster and vector data

    #Plot the index_da to see CRS
    index_da.plot(
        cbar_kwargs={"label": place},
        robust=True)
    plt.gca().set(
        title = f'{place} {index}',
        xlabel='',
        ylabel='')
    plt.show()

# plot_index(index_da, place)

def plot_gdf_da(place_gdf, index_da, edgecolor='black', cmap='terrain'):
    """
    Overlay gdf on da map.
    
    Default `cmap` is 'viridis`;
    See <https://matplotlib.org/stable/users/explain/colors/colormaps.html>.

    Args:
        place_gdf (gdf): gdf for place
        index_da (da): index for place
        edgecolor (char, optional): Name of color for edges of gdf
        cmap (char, optional): color map
    """
    import cartopy.crs as ccrs # CRSs
    import matplotlib.pyplot as plt # Overlay raster and vector data

    # Plot index.
    index_da = index_da.rio.reproject(ccrs.Mercator())
    index_da.plot(vmin=0, robust=True, cmap=cmap)
    # Plot place outline
    for idx in range(0, len(place_gdf)):
      #print(buffalo_gdf.iloc[[idx]])
      place_idx_gdf = place_gdf.iloc[[idx]].to_crs(ccrs.Mercator())
      # Use color column from place_gdf if provided
      if 'color' in place_idx_gdf.columns:
          edgecolor = place_idx_gdf['color'].values[0]
      place_idx_gdf.boundary.plot(ax=plt.gca(), color=edgecolor)
    # Strip labels and ticks of and plot.
    plt.gca().set(
        xlabel='', ylabel='', xticks=[], yticks=[])
    plt.show()

# plot_gdf_da(place_gdf, index_da)

def plot_gdf_state(place_gdf, aiannh=False):
    """
    Plot overlay of redlining GeoDataFrame with state boundaries.

    Args:
        place_gdf (gdf): gdf with redlining cities
        aiannh (bool, optional): include AIANNH boundaries if True 
    Returns:
        cropped_da (da): Processed raster da
    """
    import matplotlib.pyplot as plt
    import geopandas as gpd # Work with vector data
    import contextily as ctx
    
    # Download state data using cenpy and read into GeoDataFrame
    state_url = "https://www2.census.gov/geo/tiger/TIGER2022/STATE/tl_2022_us_state.zip"
    states_gdf = gpd.read_file(state_url)
    
    if aiannh:
        aiannh_url = "https://www2.census.gov/geo/tiger/TIGER2022/AIANNH/tl_2022_us_aiannh.zip"
        aiannh_gdf = gpd.read_file(aiannh_url)

    # Calculate the bounding box
    bbox = place_gdf.total_bounds
    xmin, ymin, xmax, ymax = bbox

    fig, ax = plt.subplots(figsize=(10, 10))
    states_gdf.boundary.plot(ax=ax, color="black", linewidth=0.5)
    if aiannh:
        aiannh_gdf.boundary.plot(ax=ax, color="red", linewidth=0.5)
    place_gdf.plot(ax=ax)
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs=place_gdf.crs.to_string())

    # Setting the bounds
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

    return plt.show()

# plot_gdf_state(place_gdf)

def plot_gdfs_map(place_gdf, column=['asthma','edge_density'], color=['Blues','Greens'], map=True):
    """
    Create Row of Plots.
    
    Args:
        place_gdf (gdf): gdf for place
        column (list, optional): list of columns to plot
        color (list, optional): list of color maps
        map (bool, optional): include map if True
    """
    import matplotlib.pyplot as plt
    import contextily as ctx

    # Make sure `column` and `color` are lists, and `color` at least as long as `column`
    if not isinstance(column, list):
        column = [column]
    n_column = len(column)
    if not isinstance(color, list):
        color = [color]
    n_color = len(color)
    if n_color == 1:
        color = (color * n_column)
    elif n_color < n_column:
        color = (color * n_color)[:n_column]

    # Create a figure with two subplots side by side
    figwidth = 12 / n_column
    fig, ax = plt.subplots(1, n_column, figsize=(12, figwidth))
    if n_column == 1:
        ax = [ax]
    cbar = []

    for i in list(range(n_column)):
        # Plot the first GeoDataFrame on the first subplot
        place_plot = place_gdf.plot(column=column[i], ax=ax[i], edgecolor="black", cmap=color[i])
        ax[i].set_title(f'{column[i].title()} Plot')
        if map:
            ctx.add_basemap(ax[i], source=ctx.providers.OpenStreetMap.Mapnik, crs=place_gdf.crs.to_string())
        cbar.append(plt.colorbar(place_plot.collections[0], ax=ax[i], orientation='horizontal'))
        cbar[i].set_label(f'{column[i].title()} Intensity')  # Set the label for the color bar

    # Show the plots
    plt.show()
    
# plot_gdfs_map(place_gdf)

def plot_das(das, titles = None, axes=['latitude', 'longitude'], gdf=None, onebar=True, cmap='terrain'):
    """
    Create rows of plots for a list of DataArrays.

    Args:
        das (list of da): List of DataArrays to plot.
        titles (list of str, optional): List of plot titles. Defaults to None.
        gdf (gdf, optional): GeoDataFrame to overlay on the plot. Defaults to None.
        onebar (bool, optional): One bar if True (default).
        cmap (str, optional): Color map. Defaults to 'terrain'.
    """
    import matplotlib.pyplot as plt
    
    # If no titles are provided, use the coordinates of the first DataArray.
    if titles is None:
        titles = das.coords[das.dims[0]].values
        
    # Set up subplots (adjust rows and columns for layout)
    fig, axes = plt.subplots(nrows=1, ncols=len(das), figsize=(20, 5), constrained_layout=True)

    plt.xlabel(axes[0])
    plt.ylabel(axes[1])

    # Loop through each da and plot in a subplot
    if gdf is not None:
        edgecolor = 'black'
    cbar = []
    if onebar:
        cbar_mappable = None  # To store the QuadMesh object for the colorbar
    for i in range(len(das)):
        da = das[i]

        # Plot the raster on the corresponding subplot
        quadmesh = da.plot(ax=axes[i], add_colorbar=False, cmap=cmap)
        axes[i].set_title(titles[i]) # Add a title to each subplot
        
        # Overlay gdf on da map if provided.
        if gdf is not None:
            gdf.boundary.plot(ax=axes[i], color="black", linewidth=0.5)
            # Plot place outline
            for idx in range(0, len(gdf)):
                idx_gdf = gdf.iloc[[idx]].to_crs(da.rio.crs)
                # Use color column from gdf if provided
                if 'color' in idx_gdf.columns:
                    edgecolor = idx_gdf['color'].values[0]
                idx_gdf.boundary.plot(ax=axes[i], color=edgecolor)

        # Individual Color Bar
        if not onebar:
            cbar.append(plt.colorbar(quadmesh, ax=axes[i], orientation='horizontal'))
            cbar[i].set_label(f'{titles[i]} Intensity')  # Set the label for the color bar
        else:
            if cbar_mappable is None:
                cbar_mappable = quadmesh

    # Global colorbar
    if onebar:
        fig.colorbar(cbar_mappable, ax=axes, orientation="horizontal", fraction=0.02, pad=0.1).set_label("Value")

    plt.show()
    
# plot_das(das)

def plot_matrix(model_df):
    """
    Plot of model matrix.

    Args:
        model_df (df): model DataFrame
    """
    import seaborn as sns
    import matplotlib.pyplot as plt

    sns.pairplot(model_df.iloc[:, [1,2,3]])
    plt.show()
    
# plot_matrix(model_df)

def plot_train_test(y_test, index='asthma'):
    """
    Plot test fit.

    Args:
        y_text (nparray): test dataset
    """
    import matplotlib.pyplot as plt
    import numpy as np


    # Plot measured vs. predicted asthma prevalence with a 1-to-1 line
    # **note: has asthma 
    y_max = y_test[index].max()
    
    x = y_test[index]
    y = y_test[f'pred_{index}']
    
    plt.scatter(x, y, alpha=0.6, linewidth=0.5)

    # Add labels and title
    plt.xlabel(f'Measured Adult {index.title()} Prevalence')
    plt.ylabel('Predicted Adult {index.title()} Prevalence')
    plt.title('Linear Regression Performance - Testing Data')

    # Set x and y limits
    plt.xlim(0, y_max)
    plt.ylim(0, y_max)

    # Add an identity line
    identity_line = np.linspace(0, y_max, 100)
    plt.plot(identity_line, identity_line, color='blue', linestyle='--', linewidth=1)
    plt.show()

# plot_train_test(y_test)

def plot_delta_gdf(delta_gdf):
    """
    Plot Delta GDF.
    
    Args:
        delta_gdf (gdf): area to overlay on topomap
    """
    import matplotlib.pyplot as plt
    import contextily as ctx

    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    delta_gdf.plot(ax=ax, edgecolor="black", color="none")
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs=delta_gdf.crs.to_string())
    
    plt.show()
    
# plot_delta_gdf(delta_gdf)

def plot_cluster(rgb_sat, model_df):
    """
    Plot of RGB and Clusters.
    
    Args:
        rgb_sat (da): rescaled to 0-255 with saturation
        model_df (df): data frame with band data and clusters
    Returns:
        cluster_hv (hvplot): pair of HV plots
    """
    import xarray as xr
    import matplotlib.pyplot as plt
    
    sh = rgb_sat.shape

    da = xr.DataArray(rgb_sat, dims=["band", "y", "x"], coords={"band": ["R", "G", "B"]})

    # Reshape the DataArray to a 2D array where each row is a pixel and columns are R, G, B values
    df = da.stack(z=("y", "x")).transpose("z", "band").to_pandas()
    df.columns = ["R", "G", "B"]
    df = df / 255

    # Reshape the DataFrame back to the original image shape for plotting
    img = df.values.reshape((sh[1], sh[2], 3))

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    ax[0].imshow(img)
    ax[0].set_title('RGB Plot')
    ax[0].axis('off')
    (
        model_df
        .clusters.to_xarray()
        .sortby(['x', 'y'])
        .plot(ax=ax[1], add_colorbar=False)
    )
    ax[1].set_title('Clusters')
    ax[1].axis('off')
    ax[1].set_aspect('equal')
    
    # Show the plots
    plt.show()

# plot_cluster(reflectance_da)