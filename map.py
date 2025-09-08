#!/usr/bin/env -S uv run --script

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pandas",
#     "geopandas",
#     "shapely",
# ]
# ///

import pandas as pd
import geopandas as gpd
from shapely import get_coordinates


def main():
    geo_df = gpd.read_file('street_centerlines.geojson')
    name_df = pd.read_csv('street_name_table.csv')
    geo_df = geo_df.merge(name_df, how='left', left_on='NEW_NM_ID', right_on='new_nm_id')

    minx, miny, maxx, maxy = geo_df.total_bounds
    geo_df['minx'], geo_df['miny'], geo_df['maxx'], geo_df['maxy'] = minx, miny, maxx, maxy
    diffx = maxx - minx
    diffy = maxy - miny
    if diffy > diffx: geo_df['scale'] = 1 / diffy
    else: geo_df['scale'] = 1 / diffx

    geo_df['svg'] = geo_df.apply(lambda r: row_to_svg(r), axis=1)

    print(geo_df.head(), end="\n\n")
    print(geo_df.columns, end="\n\n")

    svg_string = '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 1 1" fill="none">'
    geo_df = geo_df.sort_values(by=['Speed'], ascending=False) # place gray roads below green roads
    for row in geo_df.iterfeatures():
        svg_string += row['properties']['svg'] + '\n'
    svg_string += '</svg>'
    with open('map.svg', 'w') as f:
        f.write(svg_string)


def row_to_svg(row):

    line = row['geometry']
    coords = get_coordinates(line)
    svg_line = 'M'
    for coord in coords:
        x = (coord[0] - row['minx']) * row['scale']
        y = (coord[1] - row['miny']) * row['scale']
        y = 1 - y # flip y because 0, 0 is top left
        svg_line += f'{x},{y} L'
    svg_line = svg_line[:-2]

    color = 'green' if row['Speed'] <= 25 else '#d8d8d8'
    width = 0.0015 if row['Speed'] <= 25 else 0.0040

    return f'<path stroke="{color}" stroke-width="{width}" d="{svg_line}"/>'


if __name__ == "__main__":
    main()