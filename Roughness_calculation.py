# -*- coding: utf-8 -*-
"""
Created on Tue May 21 14:22:24 2024

@author: jettr and jamel
"""

#%%
import rasterio as rio
from rasterio.enums import Resampling
from rasterio.plot import show, show_hist

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


if not os.path.exists('roughness2009.tif'):
    gdal.DEMProcessing("roughness2009.tif" , 'DEM2009_cropped_edges.tif' ,"roughness", computeEdges=True)
else:
    print('File already exists, skipping roughness calculation')


roughness_2009 = gdal.Open('roughness2009.tif')
roughness_2009_array = roughness_2009.ReadAsArray()

#%%

# Plotting 2009 Slope shade

# Crop region
xmin = 1000
xmax = 2000
ymin = 900
ymax = 1500


max_value2009 = np.nanmax(roughness_2009_array)
min_value2009 = np.nanmin(roughness_2009_array)

plt.figure()
plt.title('2009 roughness Raster')
plt.imshow(roughness_2009_array[ymin:ymax, xmin:xmax])
plt.colorbar(label='Roughness')
plt.clim(min_value2009, 8)
plt.show()

#%%

plt.figure()
show_hist(roughness_2009_array)
plt.show()

#%%



if not os.path.exists('roughness2017.tif'):
    gdal.DEMProcessing("roughness2017.tif" , 'output_be.tif' ,"roughness", computeEdges=True)
else:
    print('File already exists, skipping roughness calculation')


roughness_2017 = gdal.Open('roughness2017.tif')
roughness_2017_array = roughness_2017.ReadAsArray()
roughness_2017_array = np.where(roughness_2017_array== -9999 , np.nan, roughness_2017_array)

#%%
plt.figure()
show_hist(roughness_2017_array)
plt.show()

#%%
# Plotting 2009 Slope shade

# Crop region
xmin = 1000
xmax = 2000
ymin = 900
ymax = 1500


max_value2009 = np.nanmax(roughness_2017_array)
min_value2009 = np.nanmin(roughness_2017_array)



plt.figure()
plt.title('2017 roughness Raster')
plt.imshow(roughness_2017_array[ymin:ymax, xmin:xmax])
plt.colorbar(label='Roughness')
plt.clim(min_value2009, 8)
plt.show()



#%%


# # Subplot for both the 2009 and the 2017 slopes

# # crop region
# xmin = 1000
# xmax = 2000
# ymin = 900
# ymax = 1500


# fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(10, 5), sharey=False, sharex=False)

# im1 = ax1.imshow(roughness_2009_array, cmap='viridis') 
# ax1.set_title('2009 roughness ')
# ax1.set_xlim(xmin - 0.5, xmax + 0.5)
# ax1.set_ylim(ymin - 0.5, ymax + 0.5)
# ax1.clim(0, 8)

# ax1.invert_yaxis()  # To ensure the origin (0,0) is at the top-left


# im2 = ax2.imshow(roughness_2017_array, cmap='viridis')
# ax2.set_title('2017 roughness ')
# ax2.set_xlim(xmin - 0.5, xmax + 0.5)
# ax2.set_ylim(ymin - 0.5, ymax + 0.5)
# ax2.clim(0, 8)
# ax2.invert_yaxis()  # To ensure the origin (0,0) is at the top-left

# cbar = fig.colorbar(im2, ax=[ax1, ax2], orientation='vertical', shrink=0.6)




# plt.show()
