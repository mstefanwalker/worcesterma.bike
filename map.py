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
    geo_df = gpd.read_file('street_centerlines.geojson')
    name_df = pd.read_csv('street_name_table.csv')
    geo_df = geo_df.merge(name_df, how='left', left_on='NEW_NM_ID', right_on='new_nm_id')

    print(geo_df.head(), end="\n\n")
    print(geo_df.columns, end="\n\n")

    for i, row in enumerate(geo_df.iterfeatures()):
        if i >= 10:
            break
        nm_id = row['properties']['NEW_NM_ID']
        speed = row['properties']['Speed']
        name = row['properties']['full_name']
        coords = row['geometry']['coordinates']
        print(f'{nm_id} {speed:2} {name:20} {str(coords)[:50]}...')


if __name__ == "__main__":
    main()