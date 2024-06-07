# -*- coding: utf-8 -*-
"""
Created on Thu May  9 11:33:51 2024

@author: jettr and jamel

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


# Cleaning the nodata values and writing to a new file


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

DEM_Cropped = gdal.Open('DEM2009_cropped_edges.tif')
DEM_Cropped_array = DEM_Cropped.ReadAsArray()

#%%

# Creating the Slope raster for 2009
# Calculates Slope in Degrees


if not os.path.exists('Slope2009.tif'):
    gdal.DEMProcessing("Slope2009.tif" , 'DEM2009_cropped_edges.tif' ,"slope", computeEdges=True)
else:
    print('File already exists, skipping slope calculation')


Slope_2009 = gdal.Open('Slope2009.tif')
Slope_2009_array = Slope_2009.ReadAsArray()

#%%

# # Plotting 2009 Slope shade

# max_value2009 = np.nanmax(Slope_2009_array)
# min_value2009 = np.nanmin(Slope_2009_array)

# plt.figure()
# plt.title('2009 Slope Raster')
# plt.imshow(Slope_2009_array)
# plt.colorbar(label='Slope')
# plt.clim(min_value2009, max_value2009)
# plt.show()

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
    gdal.DEMProcessing("Slope2017.tif" , 'DEM_Post2017_edges.tif' ,"slope", computeEdges=True)
else:
    print('File already exists, skipping slope calculation')



Slope_2017 = gdal.Open('Slope2017.tif')
Slope_2017_array = Slope_2017.ReadAsArray()

#%%

# # Plotting 2017 Slope shade

# max_value2017 = np.nanmax(Slope_2017_array)
# min_value2017 = np.nanmin(Slope_2017_array)

# plt.figure()
# plt.title('2017 Slope Raster')
# plt.imshow(Slope_2017_array)
# plt.colorbar(label='Slope')
# plt.clim(min_value2017, max_value2017)
# plt.show()


#%%

# Subplot for both the 2009 and the 2017 slopes

xmin = 1050  
xmax = 1800  
ymin = 950  
ymax = 1400 


fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(10, 5), sharey=False, sharex=False)

im1 = ax1.imshow(Slope_2009_array, cmap='viridis') 
ax1.set_title('2009 Slope ')
ax1.set_xlim(xmin, xmax)
ax1.set_ylim(ymin, ymax)
ax1.invert_yaxis()  # To ensure the origin (0,0) is at the top-left


im2 = ax2.imshow(Slope_2017_array, cmap='viridis')
ax2.set_title('2017 Slope ')
ax2.set_xlim(xmin, xmax)
ax2.set_ylim(ymin, ymax)
ax2.invert_yaxis()  # To ensure the origin (0,0) is at the top-left

cbar = fig.colorbar(im2, ax=[ax1, ax2], orientation='vertical', shrink=0.6)




plt.show()

#%%

xmin = 1050  
xmax = 1800  
ymin = 950  
ymax = 1400 

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

im1 = ax1.imshow(Slope_2009_array, cmap='viridis')
ax1.set_title('2009 Slope')

im2 = ax2.imshow(Slope_2017_array, cmap='viridis')
ax2.set_title('2017 Slope')

im3 = ax3.imshow(Slope_2009_array[ymin:ymax, xmin:xmax], cmap='viridis')


im4 = ax4.imshow(Slope_2017_array[ymin:ymax, xmin:xmax], cmap='viridis')



# Create a single colorbar for all subplots
cbar = fig.colorbar(im2, ax=[ax1, ax2, ax3, ax4], orientation='vertical', shrink=0.6)

plt.subplots_adjust(left=0.1,bottom=0.01,right=0.75,top=0.9,wspace=0.2,hspace=-0.4)
plt.show()


#%%



Slope_Diff = Slope_2017_array - Slope_2009_array


#%%
# Path to the output raster file
output_path = 'Slope_Diff.tif'

# Check if the output file already exists
if not os.path.exists(output_path):
    # Read the metadata from one of the original DEMs (e.g., DEM 2009 cropped)
    with rio.open('Slope2009.tif') as src:
        meta = src.meta.copy()

    # Update the metadata to reflect the new data type and no-data value if necessary
    meta.update({
        'dtype': 'float32',  # Update the data type if needed
        'nodata': np.nan     # Set the no-data value if needed
    })

    # Write the Difference_Array to a new raster file
    with rio.open(output_path, 'w', **meta) as dst:
        dst.write(Slope_Diff.astype('float32'), 1)  # Write the data to the first band

    print(f"Difference DEM written to {output_path}")
else:
    print(f"File {output_path} already exists. Skipping writing.")
    
    
#%%

# Plotting Difference in Slope Shades


with rio.open('Slope_Diff.tif') as src:
    Diff_data = src.read(1)

max_value_diff = np.nanmax(Diff_data)
min_value_diff = np.nanmin(Diff_data)
# Define the zoomed-in extent (adjust these values as needed)

# crop region
xmin = 1050
xmax = 1800
ymin = 950
ymax = 1400


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# full Slope Difference
im1 = ax1.imshow(Diff_data, cmap='bwr_r')
ax1.set_title('Slope Difference')
fig.colorbar(im1, ax=ax1, label='Slope',shrink=0.6)
im1.set_clim(-max_value_diff, max_value_diff)

# cropped Slope Difference
im2 = ax2.imshow(Diff_data, cmap='bwr_r')
ax2.set_title('Slope Difference DEM (Cropped)')
fig.colorbar(im2, ax=ax2, label='Slope', shrink=0.6)
im2.set_clim(-max_value_diff,max_value_diff)
ax2.set_xlim(xmin - 0.5, xmax + 0.5)
ax2.set_ylim(ymin - 0.5, ymax + 0.5)
ax2.invert_yaxis()  # To ensure the origin (0,0) is at the top-left


plt.show()

#%%

with rio.open('Slope_Diff.tif') as src:
    Diff_data = src.read(1)

max_value_diff = np.nanmax(Diff_data)
min_value_diff = np.nanmin(Diff_data)

# crop region
xmin = 1050
xmax = 1800
ymin = 950
ymax = 1400


plt.figure()

im = plt.imshow(Diff_data, cmap='bwr_r')
plt.title('Slope Difference DEM (Cropped)')
cbar = plt.colorbar(im, label='Slope', shrink=0.75)
im.set_clim(-max_value_diff, max_value_diff)
plt.xlim(xmin - 0.5, xmax + 0.5)
plt.ylim(ymin - 0.5, ymax + 0.5)
plt.gca().invert_yaxis()
plt.show()


