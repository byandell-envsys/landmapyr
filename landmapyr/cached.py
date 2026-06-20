def cached(func_key, override=False):
    """
    A decorator to cache function results.
    
    The decorator loads a cached pickle file
    in the `jars` directory under the `HOME` directory
    if it already exists
    and the `override` argument is set to `False`,
    or computes the decorated function and caches the results.
    The decorator names the pickle file as 'f{func_key}.pickle'.
    If a key word `cache_key` is an argument in the decorated function,
    it is used to alter the file name to 'f{func_key}_{cache_key}.pickle'.
    This `cache_key` keyword is detected by the decorator via `**kwargs`.
    Args:
      func_key (str): File basename used to save pickled results
      override (bool): When True, re-compute even if the results are already stored
    """
    def compute_and_cache_decorator(compute_function):
        """
        Wrap the caching function
        
        Args:
          compute_function (function): function to run and cache results
        Returns:
          compute_and_cache_decorator( decorator): decorator
        """
        def compute_and_cache(*args, **kwargs):
            """
            Perform a computation and cache, or load cached result.
            
            Args:
              args (list): Positional arguments for the compute function
              kwargs (list): Keyword arguments for the compute function
            """
            import os
            import pickle
            import earthpy as et

            # Add an identifier from the particular function call
            if 'cache_key' in kwargs:
                key = '_'.join((func_key, kwargs['cache_key']))
            else:
                key = func_key

            path = os.path.join(
                et.io.HOME, et.io.DATA_NAME, 'jars', f'{key}.pickle')
            
            # Check if the cache exists already or override caching
            if not os.path.exists(path) or override:
                # Make jars directory if needed
                os.makedirs(os.path.dirname(path), exist_ok=True)
                
                # Run the compute function as the user did
                result = compute_function(*args, **kwargs)
                
                # Pickle the object
                with open(path, 'wb') as file:
                    pickle.dump(result, file)
            else:
                # Unpickle the object
                with open(path, 'rb') as file:
                    result = pickle.load(file)
                    
            return result
        
        return compute_and_cache
    
    return compute_and_cache_decorator
