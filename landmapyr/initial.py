"""
Initialize Functions.

robust_code: Make code robust to interruptions
create_data_dir: Create Data Directory if it does not exist
"""
def robust_code():
    """
    Make code robust to interruptions.
    """
    import os
    import warnings
        
    warnings.simplefilter('ignore')

    # Prevent GDAL from quitting due to momentary disruptions
    os.environ["GDAL_HTTP_MAX_RETRY"] = "5"
    os.environ["GDAL_HTTP_RETRY_DELAY"] = "1"

def create_data_dir(new_dir='habitat'):
    """
    Create Data Directory if it does not exist.

    Args:
        new_dir (char, optional): Name of new directory
    Returns:
        data_dir (char): path to new directory
    """
    import os
    import pathlib

    data_dir = os.path.join(
        pathlib.Path.home(),
        'earth-analytics',
        'data',
        new_dir
    )
    os.makedirs(data_dir, exist_ok=True)

    return data_dir

# data = create_data_dir('habitat')

