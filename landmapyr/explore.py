"""
Explore Functions using Sci-Kit Learn.

index_tree: Convert categories to numbers
ramp_logic: Fuzzy ramp logic
var_trans: Variable Selection and Transformation
train_test: Model fit using train and test sets
"""
def index_tree(redlining_index_gdf):
    """
    Convert categories to numbers.
            
    Args:
        redlining_index_gdf (gdf): gdf with zonal stats
    Returns:
        tree_classifier (decision_tree): Decision tree for classifier
    """
    from sklearn.tree import DecisionTreeClassifier

    redlining_index_gdf['grade_codes'] = (
        redlining_index_gdf.grade.cat.codes)

    # Fit model
    tree_classifier = DecisionTreeClassifier(max_depth=2).fit(
        redlining_index_gdf[['mean']],
        redlining_index_gdf.grade_codes)
    
    return tree_classifier

# tree_classifier = index_tree(redlining_index_gdf)

def ramp_logic(data, up = (), down = ()):
    """
    Fuzzy ramp logic.

    Args:
        data (da): da with land measurements
        up, down (list of floats, optional): Either 1 (cliff) or 2 (ramp) values for fuzzy on-off
    Returns:
        fuzzy_data (da): Ramp with values between 0 and 1
    """
    import xarray as xr

    # Apply fuzzy logic: data > ramps[0] but it could be < ramps[1] with a ramp
    def ramp(data, fuzzy_data, up, sign=1.0):
        if(isinstance(up, float) | isinstance(up, int)):
            up = (up,)
        if(len(up)):
            fuzzy_data = fuzzy_data * (sign * data >= sign * max(up))
            if(len(up) > 1):
                up = sorted(up[:2])
                diff = up[1] - up[0]
                if(diff > 0):
                    ramp_mask = (data > up[0]) & (data <= up[1])
                    fuzzy_data = fuzzy_data + sign * ramp_mask * (data - up[0]) / diff
        return fuzzy_data

    # Set `fuzzy_data` to 1.0.
    fuzzy_data = xr.full_like(data, 1.0)
    # Ramp up.
    fuzzy_data = ramp(data, fuzzy_data, up, 1.0)
    # Ramp down.
    fuzzy_data = ramp(data, fuzzy_data, down, -1.0)

    return fuzzy_data

# data = x = xr.DataArray([float(i) for i in  range(21)])
# ramp_logic(data, (5.0, 10.0), 15)

def var_trans(ndvi_cdc_gdf):
    """
    Variable Selection and Transformation

    Args:
        ndvi_cdc_gdf (gdf): combined CDC and NDVI gdf
    Returns:
        model_df (df): model DataFrame
    """
    import numpy as np
    
    # Variable selection and transformation
    model_df = (
        ndvi_cdc_gdf
        .copy()
        [['frac_veg', 'asthma', 'mean_patch_size', 'edge_density', 'geometry']]
        .dropna()
    )

    model_df['log_asthma'] = np.log(model_df.asthma)
    
    return model_df

# model_df = var_trans(ndvi_cdc_gdf)

def train_test(model_df, resp='asthma', trans='log', test_size=0.33, random_state=42):
    """
    Model fit using train and test sets.

    Args:
        model_df (df): model DataFrame
        resp (str, optional): column name of response
        trans (str, optional): transformation of response
        test_size (float, optional): proportion test size
        random_state (int, optional): random number state
    Returns:
        y_text (nparray): test dataset
        reg (LinearRegression): LinearRegression object
        model_df (df): model DataFrame with added `pred` and `resid` columns
    """
    import numpy as np
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split

    # Select predictor and outcome variables

    X = model_df[['edge_density', 'mean_patch_size']]
    y = model_df[[f'{trans}_{resp}']]

    # Split into training and testing datasets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state)

    # Fit a linear regression
    reg = LinearRegression()
    reg.fit(X_train, y_train)

    # Predict asthma values for the test dataset
    y_test[f'pred_{resp}'] = np.exp(reg.predict(X_test))
    y_test[resp] = np.exp(y_test[f'{trans}_{resp}'])
    
    # Predict index values for all data to get `resid`
    model_df['pred'] = np.exp(reg.predict(model_df[['edge_density', 'mean_patch_size']]))
    model_df['resid'] = model_df['pred'] - model_df[f'{trans}_{resp}']

    
    return y_test, reg, model_df

# y_test, reg, model_df = trait_test(model_df)
