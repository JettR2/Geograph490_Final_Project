# -*- coding: utf-8 -*-
"""
Created on Sun May 19 10:49:47 2024

@author: jettr
"""
#%%


import os
import rasterio as rio
import whitebox
import numpy as np
import matplotlib.pyplot as plt


#%%

# set your working directory
working_directory = 'C:/Users/jettr/Dropbox (University of Oregon)/ESP_Research/Python Files/'

os.chdir(working_directory)

current_working_directory = os.getcwd()

files_in_directory = os.listdir(current_working_directory)

print("Files and directories in the current working directory:")
for item in files_in_directory:
    print(item)


#%%


# Path to the 2017 DEM
path2017 = 'output_be.tif'


# Load the DEM
with rio.open(path2017) as src:
    dem_2017 = src.read(1)
    transform = src.transform
    crs = src.crs
    nodata = src.nodata
    if nodata is not None:
        dem_2017 = np.where(dem_2017 == nodata, np.nan, dem_2017)
        plt.imshow(dem_2017)


#%%


# Save the DEM as a temporary file to use with whitebox tools
tmp_dem_path = 'tmp_dem_2017.tif'
with rio.open(tmp_dem_path, 'w', **src.meta) as dst:
    dst.write(dem_2017, 1)



wbt = whitebox.WhiteboxTools()


#%%


# Fill depressions
filled_dem_path = 'filled_dem_2017.tif'
wbt.fill_depressions(tmp_dem_path, filled_dem_path)



# Calculate flow direction
flow_dir_path = 'flow_direction_2017.tif'
wbt.d8_pointer(filled_dem_path, flow_dir_path)



# Calculate flow accumulation
flow_acc_path = 'flow_accumulation_2017.tif'
wbt.d8_flow_accumulation(flow_dir_path, flow_acc_path)


#%%


# Load the results for visualization
with rio.open(flow_acc_path) as src:
    flow_accumulation = src.read(1)


# Visualize the flow accumulation
plt.figure(figsize=(10, 8))
plt.imshow(np.log1p(flow_accumulation), cmap='cubehelix', interpolation='none')
plt.colorbar(label='Log Flow Accumulation')
plt.title('Flow Accumulation')
plt.show()

# Cleanup temporary files
os.remove(tmp_dem_path)


