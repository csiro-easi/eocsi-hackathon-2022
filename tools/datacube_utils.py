#!python3

# A collection of utilities that can be used in with the Open Data Cube API.
#
# License: Apache 2.0

# Created for EASI Hub training notebooks, https://dev.azure.com/csiro-easi/easi-hub-public/_git/hub-notebooks
# Mostly redundent since dea_tools was released on github and added to EASI images.

import numpy as np
import math
import folium
from pyproj import Transformer
from collections import Counter
import geopandas as gpd
import xarray as xr
import rasterio.features
from datacube.utils.cog import write_cog


# Commented-out: Not sure there's a significant enough difference with this version
# def mostcommon_crs(dc, product, query):
#     """Adapted from https://github.com/GeoscienceAustralia/dea-notebooks/blob/develop/Tools/dea_tools/datahandling.py
    
#     Changes include:
#     - product can be defined in query
#     - return a warning rather than ValueError if no CRS is found
#     """
#     q = dict(query)
#     if not product and 'product' in q:
#         product = q['product']
#     if 'product' in q:
#         del q['product']
#     if isinstance(product, list):
#         matching_datasets = []
#         for i in product:
#             matching_datasets.extend(dc.find_datasets(product=i, **query))        
#     else:
#         matching_datasets = dc.find_datasets(product=product, **query)
#     crs_list = [str(i.crs) for i in matching_datasets]
#     crs_mostcommon = None
#     if len(crs_list) > 0:
#         # Identify most common CRS
#         crs_counts = Counter(crs_list)
#         crs_mostcommon = crs_counts.most_common(1)[0][0]
#     else:
#         logger.warning('No data was found for the supplied product query')
#     return crs_mostcommon


# Borrowed from https://github.com/GeoscienceAustralia/dea-notebooks/blob/develop/Tools/dea_tools/plotting.py
# def display_map(x, y, crs='EPSG:4326', margin=-0.5, zoom_bias=0):
#     """
#     Changes:
#     - use pyproj 2 Transformer, see https://pyproj4.github.io/pyproj/stable/gotchas.html#upgrade-transformer
#     """

#     # Convert each corner coordinates to lat-lon
#     points = [ (x[0],y[0]), (x[1],y[0],), (x[0],y[1]), (x[1],y[1]) ]
#     transformer = Transformer.from_crs(crs, 'EPSG:4326')
#     tmp = np.array( list(transformer.itransform(points)) )
#     all_longitude = tmp[:,0]; all_latitude = tmp[:,1]

#     ....

