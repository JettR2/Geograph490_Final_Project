# -*- coding: utf-8 -*-
"""
Created on Sun May 19 10:49:47 2024

@author: jettr and jamel
"""
#%%

import os
import rasterio as rio
import whitebox
import numpy as np
import matplotlib.pyplot as plt

# Set working directory
working_directory = 'C:/Users/jettr/Dropbox (University of Oregon)/ESP_Research/Python Files/'
os.chdir(working_directory)

# Load DEM
path2017 = 'output_be.tif'
with rio.open(path2017) as src:
    dem_2017 = src.read(1)
    transform = src.transform
    crs = src.crs
    nodata = src.nodata
    if nodata is not None:
        dem_2017 = np.where(dem_2017 == nodata, np.nan, dem_2017)
        
# Save DEM as temporary file for WhiteboxTools
tmp_dem_path = os.path.join(working_directory, 'tmp_dem_2017.tif')
with rio.open(tmp_dem_path, 'w', **src.meta) as dst:
    dst.write(dem_2017, 1)

# Verify that the temporary DEM file exists
if not os.path.exists(tmp_dem_path):
    raise FileNotFoundError(f"Temporary DEM file not found: {tmp_dem_path}")

# Initialize WhiteboxTools
wbt = whitebox.WhiteboxTools()
wbt.set_working_dir(working_directory)

# Fill depressions
filled_dem_path = os.path.join(working_directory, 'filled_dem_2017.tif')
wbt.fill_depressions(tmp_dem_path, filled_dem_path)

# Verify that the filled DEM file exists
if not os.path.exists(filled_dem_path):
    raise FileNotFoundError(f"Filled DEM file not found: {filled_dem_path}")

# Calculate flow direction
flow_dir_path = os.path.join(working_directory, 'flow_direction_2017.tif')
wbt.d8_pointer(filled_dem_path, flow_dir_path)

# Verify that the flow direction file exists
if not os.path.exists(flow_dir_path):
    raise FileNotFoundError(f"Flow direction file not found: {flow_dir_path}")

# Calculate flow accumulation
flow_acc_path = os.path.join(working_directory, 'flow_accumulation_2017.tif')
wbt.d8_flow_accumulation(flow_dir_path, flow_acc_path)

# Verify that the flow accumulation file exists
if not os.path.exists(flow_acc_path):
    raise FileNotFoundError(f"Flow accumulation file not found: {flow_acc_path}")

# Calculate streams
streams_path = os.path.join(working_directory, 'streams_2017.tif')
stream_threshold = 1000  # Adjust this threshold based on your DEM resolution and area
wbt.extract_streams(flow_acc_path, streams_path, threshold=stream_threshold)

# Verify that the streams file exists
if not os.path.exists(streams_path):
    raise FileNotFoundError(f"Streams file not found: {streams_path}")

# Calculate watershed basins
watershed_basins_path = os.path.join(working_directory, 'watershed_basins_2017.tif')
wbt.watershed(flow_dir_path, streams_path, watershed_basins_path)

# Verify that the watershed basins file exists
if not os.path.exists(watershed_basins_path):
    raise FileNotFoundError(f"Watershed basins file not found: {watershed_basins_path}")

# Load results for visualization
with rio.open(flow_acc_path) as src:
    flow_accumulation = src.read(1)

with rio.open(streams_path) as src:
    streams = src.read(1)

with rio.open(watershed_basins_path) as src:
    watershed_basins = src.read(1)

# Visualize flow accumulation
plt.figure(figsize=(10, 8))
plt.imshow(np.log1p(flow_accumulation), cmap='cubehelix', interpolation='none')
plt.colorbar(label='Log Flow Accumulation')
plt.title('Flow Accumulation')
plt.show()

# Visualize streams
plt.figure(figsize=(10, 8))
plt.imshow(streams, cmap='Blues', interpolation='none')
plt.colorbar(label='Stream Order')
plt.title('Extracted Streams')
plt.show()

# Visualize watershed basins
plt.figure(figsize=(10, 8))
plt.imshow(watershed_basins, cmap='tab20b', interpolation='none')
plt.colorbar(label='Watershed Basins')
plt.title('Watershed Basins')
plt.show()

# Cleanup temporary files
os.remove(tmp_dem_path)
os.remove(filled_dem_path)
os.remove(flow_dir_path)
os.remove(flow_acc_path)
os.remove(streams_path)
os.remove(watershed_basins_path)


