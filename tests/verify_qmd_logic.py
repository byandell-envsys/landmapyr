import sys
import os
sys.path.append(os.getcwd())
from landmapy.usgs import find_usgs_site, get_site_metadata

def verify():
    print("Searching for: White River near Oglala in SD")
    sites = find_usgs_site("White River near Oglala", "SD")
    if not sites.empty:
        site_info = sites.iloc[0]
        site_id = site_info['site_no']
        print(f"Found: {site_info['station_nm']} ({site_id})")
        
        print(f"Fetching metadata for: {site_id}")
        meta = get_site_metadata(site_id)
        print(f"Parameters: {meta['parameters']}")
        print(f"Dates: {meta['start_date']} to {meta['end_date']}")
        
        # Check if we have parameters and dates
        if meta['parameters'] and meta['start_date'] and meta['end_date']:
            print("Success: Dynamic metadata retrieval works.")
        else:
            print("Failure: Metadata is missing components.")
    else:
        print("Failure: No site found.")

if __name__ == "__main__":
    verify()
