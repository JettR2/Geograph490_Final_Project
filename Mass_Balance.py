# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:16:22 2024

@author: jettr
"""
#%%

import os
import rasterio as rio
from rasterio.windows import Window
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize

# Set working directory
working_directory = 'C:/Users/jettr/Dropbox (University of Oregon)/ESP_Research/Python Files/'
os.chdir(working_directory)

# Print files in the working directory
print("Files and directories in the current working directory:")
for item in os.listdir(os.getcwd()):
    print(item)

#%%


# Load the Difference DEM
diffmap_path = 'Difference_DEM.tif'
diffmap = rio.open(diffmap_path)
diffarray = diffmap.read(1)

# Load the Post-slide DEM
post_slide_dem_path = 'Slope2017.tif'
post_slide_dem = rio.open(post_slide_dem_path)
post_slide_array = post_slide_dem.read(1)

#%%
# Define the zoomed-in extent
xmin, xmax = 1050, 1800
ymin, ymax = 950, 1400

# Crop the rasters to the specified extent
window = Window.from_slices((ymin, ymax), (xmin, xmax))
cropped_diffarray = diffmap.read(1, window=window)
cropped_post_slide_array = post_slide_dem.read(1, window=window)

#%%

# Separate the negative and positive values into different arrays
negative_values = np.where(cropped_diffarray < 0, cropped_diffarray, 0)
positive_values = np.where(cropped_diffarray > 0, cropped_diffarray, 0)

# Calculate the area and volume of the landslide
pixel_size = diffmap.res[0] * diffmap.res[1]  # Assuming square pixels

area_positive = np.sum(positive_values > 0) * pixel_size
volume_positive = np.sum(positive_values) * pixel_size

area_negative = np.sum(negative_values < 0) * pixel_size
volume_negative = abs(np.sum(negative_values) * pixel_size)

# Calculate the mass balance
mass_balance = volume_positive - volume_negative
total_changed_area = area_positive + area_negative
#%%

# Function to plot DEM with overlay
def plot_dem_with_overlay(base_array, overlay_array, title, cmap, vmin, vmax, cbar_label):
    plt.figure(figsize=(10, 8))
    plt.title(title)
    plt.imshow(base_array, cmap='gray')
    plt.imshow(overlay_array, cmap=cmap, alpha=0.55, norm=Normalize(vmin=vmin, vmax=vmax))
    cbar = plt.colorbar(label=cbar_label, shrink=0.6)
    plt.show()

# Plot the cropped Post-slide DEM with the cropped Difference DEM on top
max_abs_value = max(abs(np.min(cropped_diffarray)), abs(np.max(cropped_diffarray)))
plot_dem_with_overlay(
    cropped_post_slide_array, cropped_diffarray,
    'Post-slide Slope DEM with Difference DEM Overlay (meters)',
    'bwr_r', -max_abs_value, max_abs_value, 'Elevation Change (meters)'
)

# Plot negative values
max_abs_value_negative = np.min(negative_values)
plot_dem_with_overlay(
    cropped_post_slide_array, negative_values,
    'Post-slide Slope DEM with Negative Difference DEM Overlay (meters)',
    'Reds_r', 0, max_abs_value_negative, 'Negative Elevation Change (meters)'
)

# Plot positive values
max_abs_value_positive = np.max(positive_values)
plot_dem_with_overlay(
    cropped_post_slide_array, positive_values,
    'Post-slide Slope DEM with Positive Difference DEM Overlay (meters)',
    'Blues', 0, max_abs_value_positive, 'Positive Elevation Change (meters)'
)

#%%
# Print area and volume calculations
print(f'Area of the Upended Block (positive values ~ Moved Mass): {area_positive*0.000001} km^2')
print(f'Volume of the Upended Block (positive values): {volume_positive} meters^3')
print('')
print(f'Area of the Slumped Block (negative values ~ Moved Mass): {area_negative*0.000001} km^2')
print(f'Volume of the Slumped Block (negative values): {volume_negative} meters^3')
print('')
print(f'Mass Balance = Positive Values + Negative Values: {mass_balance} meters^3')
print(f'Total Changed Area {total_changed_area} m^2 or {total_changed_area*0.000001} km^2')
# Close the datasets
diffmap.close()
post_slide_dem.close()
