# -*- coding: utf-8 -*-
"""
Created on Thu May  9 11:33:51 2024

@author: jettr
"""
#%%


import rasterio as rio
from rasterio.enums import Resampling
from rasterio.plot import show

import os
from osgeo import gdal


import matplotlib.pyplot as plt
import numpy as np




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

postslidedem2017 = rio.open('output_be.tif')
preslidedem2009 = rio.open('DEM2009_cropped.tif') # The reprojected and cropped DEM

preslidedem2009_array = preslidedem2009.read()

postslidedem2017_array = postslidedem2017.read()

#%%
  
        
# Check if the computed edges file already exists

if not os.path.exists('DEM2009_cropped_edges.tif'):
    # Open the DEM dataset with Rasterio
    with rio.open('DEM2009_cropped.tif') as dem_src:
        # Read DEM as array
        dem2009_data = dem_src.read(1)  

        # Replace nodata values with NaN
        dem2009_data[dem2009_data == dem_src.nodata] = np.nan

        # Write the modified DEM data to a new GeoTIFF file
        with rio.open('DEM2009_cropped_edges.tif', 'w', **dem_src.profile) as slope_dem:
            slope_dem.write(dem2009_data, 1)
else:
    print("File already exists, skipping edges calculation for 2009.")

#%%

if not os.path.exists('Slope2009.tif'):
    Slope_2009 = gdal.DEMProcessing("Slope2009.tif" , 'DEM2009_cropped_edges.tif' ,"slope", computeEdges=True)
else:
    print('File already exists, skipping slope calculation')

Slope_2009_array = Slope_2009.ReadAsArray()

#%%

max_value2009 = np.nanmax(Slope_2009_array)
min_value2009 = np.nanmin(Slope_2009_array)

plt.figure()
plt.title('2009 Slope Raster')
plt.imshow(Slope_2009_array)
plt.colorbar(label='Slope')
plt.clim(min_value2009, max_value2009)
plt.show()

#%%

# Check if the output file already exists
if not os.path.exists('DEM_Post2017_edges.tif'):
    # Open the DEM dataset with Rasterio
    with rio.open('output_be.tif') as dem_src:
        # Read DEM as array
        dem2017_data = dem_src.read(1)  

        # Replace nodata values with NaN
        dem2017_data[dem2017_data == dem_src.nodata] = np.nan

        # Write the modified DEM data to a new GeoTIFF file
        with rio.open('DEM_Post2017_edges.tif', 'w', **dem_src.profile) as slope_dem:
            slope_dem.write(dem2017_data, 1)
else:
    print("File already exists, skipping edges calculation for 2017.")
    
#%%

if not os.path.exists('Slope2017.tif'):
    Slope_2017 = gdal.DEMProcessing("Slope2017.tif" , 'DEM_Post2017_edges.tif' ,"slope", computeEdges=True)
else:
    print('File already exists, skipping slope calculation')

Slope_2017_array = Slope_2017.ReadAsArray()

#%%

max_value2017 = np.nanmax(Slope_2017_array)
min_value2017 = np.nanmin(Slope_2017_array)

plt.figure()
plt.title('2017 Slope Raster')
plt.imshow(Slope_2017_array)
plt.colorbar(label='Slope')
plt.clim(min_value2017, max_value2017)
plt.show()

#%%

fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(10, 5), sharey=False, sharex=False)

im1 = ax1.imshow(Slope_2009_array, cmap='viridis') 
im2 = ax2.imshow(Slope_2017_array, cmap='viridis')

cbar = fig.colorbar(im2, ax=[ax1, ax2], orientation='vertical', shrink=0.6)

ax1.set_title('2009 Slope ')
ax2.set_title('2017 Slope ')

plt.show()