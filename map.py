#!/usr/bin/env -S uv run --script

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pandas",
#     "geopandas",
# ]
# ///

import pandas as pd
import geopandas as gpd


def main():
    gdf = gpd.read_file('street_centerlines.geojson')
    print(gdf.head(), end="\n\n")

    df = pd.read_csv('street_name_table.csv')
    print(df.head(), end="\n\n")

    for i, row in enumerate(gdf.iterfeatures()):
        if i >= 10:
            break
        nm_id = row['properties']['NEW_NM_ID']
        speed = row['properties']['Speed']
        name = df.loc[df['new_nm_id'] == nm_id, 'full_name'].to_string(header=False, index=False)
        coords = row['geometry']['coordinates']
        print(f'{nm_id} {speed:2} {name:20} {str(coords)[:50]}...')


if __name__ == "__main__":
    main()