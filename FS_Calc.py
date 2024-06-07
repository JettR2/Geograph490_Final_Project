# -*- coding: utf-8 -*-
"""
Created on Mon May 20 14:52:38 2024

@author: jettr and jamel
"""

#%%

import rasterio as rio
import rioxarray as rxr

import os 

import numpy as np 
import matplotlib.pyplot as plt
from scipy.stats import mode


#%%


# Set your working directory
working_directory = 'C:/Users/jettr/Dropbox (University of Oregon)/ESP_Research/Python Files/'
os.chdir(working_directory)

current_working_directory = os.getcwd()

files_in_directory = os.listdir(current_working_directory)

print("Files and directories in the current working directory:")
for item in files_in_directory:
    print(item)
    
#%%


# Load the slope raster
slope_path = 'Slope2009.tif'
with rio.open(slope_path) as slope_src:
    slope_data = slope_src.read(1)
    slope_data = np.where(slope_data == slope_src.nodata, np.nan, slope_data)  # Handle nodata values
    transform = slope_src.transform
    crs = slope_src.crs
    


# Load the DEM for extent and resolution
dem_path = 'DEM2009_cropped.tif'
dem = rxr.open_rasterio(dem_path, masked=True).squeeze()


#%%

# Parameters for FoS calculation
cohesion = 1000  # in Pascals
soil_density = 2000  # kg/m^3
gravity = 9.81  # m/s^2
soil_depth = 10  # meters
friction_angle = 30  # degrees
# These ones will be the same for both 2009 and 2017


# These ones will change for the 2009 and the 2017 data sets
friction_angle_rad = np.deg2rad(friction_angle)
slope_rad = np.deg2rad(slope_data)

# Calculate numerator and denominator
numerator = cohesion + (soil_density * gravity * soil_depth * np.cos(slope_rad)**2 * np.tan(friction_angle_rad))
denominator = soil_density * gravity * soil_depth * np.sin(slope_rad) * np.cos(slope_rad)

# Avoid division by zero by adding a small epsilon value to the denominator
epsilon = 1e-10
denominator = np.where(denominator == 0, epsilon, denominator)


fos = numerator / denominator


# Greater view for the histogram
fos_hist_large = np.where((fos >= 0) & (fos <= 100), fos, np.nan)

# Little zoom in on the more interesting values 
fos_hist_small = np.where((fos >= 0) & (fos <= 5), fos, np.nan)

# Values Near slope instability
fos = np.where((fos > 0) & (fos < 3), fos, np.nan)  # FoS typically ranges from 0 to 10, extend to 100 for safety


#%%

# Create subplots for the histograms looking at all the data and the more interesting values within the set
fig, axs = plt.subplots(2, figsize=(10, 8))




# Plot histogram of large FoS values
axs[0].hist(fos_hist_large[~np.isnan(fos_hist_large)].flatten(), bins=50, color='blue', alpha=0.7, density=True) # Remove nan values, true/false nan values, flatten used to 
# reduce dimensions of array from 2 to 1, so that it can be plotted on the historgram

# Get the histogram data for large FoS values
counts_large, bins_large, _ = axs[0].hist(fos_hist_large[~np.isnan(fos_hist_large)].flatten(), bins=50, color='blue', alpha=0.0, density=True)
# counts_large is a length 50 array with values of ? , bins_large is a length 50 array with values of the sum proportion of that bin, bin 50 = 100


# Find the index of the bin where FoS > 2 for large FoS values
index_large = np.argmax(bins_large > 2)

# Set the colors of the bins based on their values for large FoS values
for i in range(len(counts_large)):
    if bins_large[i] <= 2:
        axs[0].fill_betweenx([0, counts_large[i]], bins_large[i], bins_large[i+1], color='red', alpha=0.7)
    else:
        axs[0].fill_betweenx([0, counts_large[i]], bins_large[i], bins_large[i+1], color='blue', alpha=0.7)

axs[0].set_title('2009 Histogram of Large FoS Values')
axs[0].set_xlabel('FoS')
axs[0].set_ylabel('Density')

# Print statistics for large FoS values
hist_max_large = np.nanmax(fos_hist_large)
hist_mean_large = np.nanmean(fos_hist_large)
hist_mode_large = mode(fos_hist_large[~np.isnan(fos_hist_large)])

print("Statistics for Large FoS Values:")
print("Max:", hist_max_large)
print("Mean:", hist_mean_large)
print("Mode:", hist_mode_large)




# Plot histogram of small FoS values

axs[1].hist(fos_hist_small[~np.isnan(fos_hist_small)].flatten(), bins=50, color='blue', alpha=0.7, density=True)

counts_small, bins_small, _ = axs[1].hist(fos_hist_small[~np.isnan(fos_hist_small)].flatten(), bins=50, color='blue', alpha=0.0, density=True)

index_small = np.argmax(bins_small > 2)

for i in range(len(counts_small)):
    if bins_small[i] <= 2:
        axs[1].fill_betweenx([0, counts_small[i]], bins_small[i], bins_small[i+1], color='red', alpha=0.7)
    else:
        axs[1].fill_betweenx([0, counts_small[i]], bins_small[i], bins_small[i+1], color='blue', alpha=0.7)

axs[1].set_title('2009 Histogram of Small FoS Values')
axs[1].set_xlabel('FoS')
axs[1].set_ylabel('Density')

hist_max_small = np.nanmax(fos_hist_small)
hist_mean_small = np.nanmean(fos_hist_small)
hist_mode_small = mode(fos_hist_small[~np.isnan(fos_hist_small)])

print("\nStatistics for Small FoS Values:")
print("Max:", hist_max_small)
print("Mean:", hist_mean_small)
print("Mode:", hist_mode_small)



plt.tight_layout()
plt.show()


#%%

# Plot the FOS on the DEM


# Parameters for FoS calculation
cohesion = 1000  # in Pascals
soil_density = 2000  # kg/m^3
gravity = 9.81  # m/s^2
soil_depth = 10  # meters
friction_angle = 30  # degrees
# These ones will be the same for both 2009 and 2017


# These ones will change for the 2009 and the 2017 data sets
friction_angle_rad = np.deg2rad(friction_angle)
slope_rad = np.deg2rad(slope_data)

# Calculate numerator and denominator
numerator = cohesion + (soil_density * gravity * soil_depth * np.cos(slope_rad)**2 * np.tan(friction_angle_rad))
denominator = soil_density * gravity * soil_depth * np.sin(slope_rad) * np.cos(slope_rad)

# Avoid division by zero by adding a small epsilon value to the denominator
epsilon = 1e-10
denominator = np.where(denominator == 0, epsilon, denominator)


fos = numerator / denominator


# Values Near slope instability
fos = np.where((fos > 0) & (fos < 3), fos, np.nan) 




# Load the DEM for extent and resolution
dem_path = 'DEM2009_cropped.tif'
dem = rxr.open_rasterio(dem_path, masked=True).squeeze()


left, bottom, right, top = dem.rio.bounds()

# Create the figure and axis
fig, ax = plt.subplots(figsize=(10, 8))

# Plot the DEM data
dem_plot = ax.imshow(dem, cmap='viridis', extent=(left, right, bottom, top))

# Plot the FoS data
fos_plot = ax.imshow(fos, cmap='RdYlGn', extent=(left, right, bottom, top), alpha=0.75)

# Add colorbars
cbar_dem = fig.colorbar(dem_plot, ax=ax, fraction=0.046, pad=0.12 , location='right')
cbar_fos = fig.colorbar(fos_plot, ax=ax, fraction=0.046, pad=0.08)

# Set colorbar labels
cbar_dem.set_label('Elevation (m)')
cbar_fos.set_label('Factor of Safety')

# Set plot title and labels
ax.set_title('2009 Factor of Safety (FoS) and DEM')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

plt.show()




#%%

output_path = 'FoS_2009_0to3.tif'


if not os.path.exists(output_path):
    # Save the FoS raster
    resolution = dem.rio.resolution()[0]  # assuming square pixels
    
    with rio.open(
        output_path,
        'w',
        driver='GTiff',
        height=fos.shape[0],
        width=fos.shape[1],
        count=1,
        dtype=fos.dtype,
        crs=crs,
        transform=transform,
    ) as dst:
        dst.write(fos, 1)
else:
    print("File already exists, skipping write out of FoS_2009_0to3 tif file.")


#%%










# For the 2017 Raster Data










#%%


# Load the 2017 slope raster
slope_path_2017 = 'Slope2017.tif'
with rio.open(slope_path_2017) as slope_src:
    slope_data_2017 = slope_src.read(1)
    slope_data_2017 = np.where(slope_data_2017 == slope_src.nodata, np.nan, slope_data_2017)  # Handle nodata values
    transform = slope_src.transform
    crs = slope_src.crs
    
#%%



# Parameters for FoS calculation
# cohesion = 1000  # in Pascals
# soil_density = 2000  # kg/m^3
# gravity = 9.81  # m/s^2
# soil_depth = 10  # meters
# friction_angle = 30  # degrees
friction_angle_rad = np.deg2rad(friction_angle)
slope_rad = np.deg2rad(slope_data_2017)

numerator = cohesion + (soil_density * gravity * soil_depth * np.cos(slope_rad)**2 * np.tan(friction_angle_rad))
denominator = soil_density * gravity * soil_depth * np.sin(slope_rad) * np.cos(slope_rad)

epsilon = 1e-10
denominator = np.where(denominator == 0, epsilon, denominator)

fos = numerator / denominator


fos_hist_large = np.where((fos >= 0) & (fos <= 100), fos, np.nan)

fos_hist_small = np.where((fos >= 0) & (fos <= 5), fos, np.nan)

fos = np.where((fos > 0) & (fos < 3), fos, np.nan)  # FoS typically ranges from 0 to 10, extend to 100 for safety



#%%

fig, axs = plt.subplots(2, figsize=(10, 8))

axs[0].hist(fos_hist_large[~np.isnan(fos_hist_large)].flatten(), bins=50, color='blue', alpha=0.7, density=True)

counts_large, bins_large, _ = axs[0].hist(fos_hist_large[~np.isnan(fos_hist_large)].flatten(), bins=50, color='blue', alpha=0.0, density=True)

index_large = np.argmax(bins_large > 2)

for i in range(len(counts_large)):
    if bins_large[i] <= 2:
        axs[0].fill_betweenx([0, counts_large[i]], bins_large[i], bins_large[i+1], color='red', alpha=0.7)
    else:
        axs[0].fill_betweenx([0, counts_large[i]], bins_large[i], bins_large[i+1], color='blue', alpha=0.7)

axs[0].set_title('2017 Histogram of FoS Values')
axs[0].set_xlabel('FoS')
axs[0].set_ylabel('Density')

hist_max_large = np.nanmax(fos_hist_large)
hist_mean_large = np.nanmean(fos_hist_large)
hist_mode_large = mode(fos_hist_large[~np.isnan(fos_hist_large)])

print("2017 Statistics for Large FoS Values:")
print("Max:", hist_max_large)
print("Mean:", hist_mean_large)
print("Mode:", hist_mode_large)

axs[1].hist(fos_hist_small[~np.isnan(fos_hist_small)].flatten(), bins=50, color='blue', alpha=0.7, density=True)

counts_small, bins_small, _ = axs[1].hist(fos_hist_small[~np.isnan(fos_hist_small)].flatten(), bins=50, color='blue', alpha=0.0, density=True)

index_small = np.argmax(bins_small > 2)

for i in range(len(counts_small)):
    if bins_small[i] <= 2:
        axs[1].fill_betweenx([0, counts_small[i]], bins_small[i], bins_small[i+1], color='red', alpha=0.7)
    else:
        axs[1].fill_betweenx([0, counts_small[i]], bins_small[i], bins_small[i+1], color='blue', alpha=0.7)

axs[1].set_title('2017 Histogram of FoS Values')
axs[1].set_xlabel('FoS')
axs[1].set_ylabel('Density')

hist_max_small = np.nanmax(fos_hist_small)
hist_mean_small = np.nanmean(fos_hist_small)
hist_mode_small = mode(fos_hist_small[~np.isnan(fos_hist_small)])

print("\n2017 Statistics for Small FoS Values:")
print("Max:", hist_max_small)
print("Mean:", hist_mean_small)
print("Mode:", hist_mode_small)

plt.tight_layout()
plt.show()


#%%


dem_path = 'output_be.tif'
dem = rxr.open_rasterio(dem_path, masked=True).squeeze()

left, bottom, right, top = dem.rio.bounds()

# Create the figure and axis
fig, ax = plt.subplots(figsize=(10, 8))

# Plot the DEM data
dem_plot = ax.imshow(dem, cmap='viridis', extent=(left, right, bottom, top))

# Plot the FoS data
fos_plot = ax.imshow(fos, cmap='RdYlGn', extent=(left, right, bottom, top), alpha=0.75)

# Add colorbars
cbar_dem = fig.colorbar(dem_plot, ax=ax, fraction=0.046, pad=0.12 , location='right')
cbar_fos = fig.colorbar(fos_plot, ax=ax, fraction=0.046, pad=0.08)

# Set colorbar labels
cbar_dem.set_label('Elevation (m)')
cbar_fos.set_label('Factor of Safety')

# Set plot title and labels
ax.set_title('2017 Factor of Safety (FoS) and DEM')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

plt.show()



#%%



output_path2017 = 'FoS_2017_0to3.tif'

if not os.path.exists(output_path2017):
    
    resolution = dem.rio.resolution()[0]
    
    with rio.open(
        output_path2017,
        'w',
        driver='GTiff',
        height=fos.shape[0],
        width=fos.shape[1],
        count=1,
        dtype=fos.dtype,
        crs=crs,
        transform=transform,
    ) as dst:
        dst.write(fos, 1)
else:
    print("File already exists, skipping write out of FoS_2017_0to3 tif file.")
