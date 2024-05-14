# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 12:58:44 2024

@author: jettr
"""
#%%


#Import packages for geospatial analysis
import rasterio as rio
from rasterio.plot import show , show_hist
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.enums import Resampling
from rasterio.transform import Affine , AffineTransformer 
from rasterio.mask import mask


#from osgeo import gdal

import os

import matplotlib.pyplot as plt
import numpy as np




#%%

# set your working directory


# Specify the path to your desired working directory
working_directory = 'C:/Users/jettr/Dropbox (University of Oregon)/ESP_Research/Python Files/'

# Change the current working directory to the specified directory
os.chdir(working_directory)


#%%

# Check WD for Files



# Get the current working directory
current_working_directory = os.getcwd()

# List all files and directories in the current working directory
files_in_directory = os.listdir(current_working_directory)

# Print the list of files and directories
print("Files and directories in the current working directory:")
for item in files_in_directory:
    print(item)




#%%



# Open the rasters to call on

DEM_2009 = rio.open('w001001.tif')
DEM_2017 = rio.open('output_be.tif')





# %%




# Take a look at the DEMs and Load the array into a Variable

#2009
Array_2009 = DEM_2009.read()
# 2017 
Array_2017 = DEM_2017.read()



print('2009 Meta Data : ', DEM_2009.meta)

print('2009 DEM Bounds : ', DEM_2009.bounds)

print('2009 DEM transform : ', DEM_2009.transform)

# The transform gives us information on the conversion of pixels to map data
# eg. 'transform': Affine(3.0, 0.0, 356956.5, 0.0, -3.0, 841198.5)
# Where
# 3.0 means each pixel represent 3  E-W geographic distance units
# 0.0 represents skewing or rotation applied to the raster. None has occured
# 356956.5 is the coordinate of the Top Left of the raster
# 0.0 again, represents skewing and rotation, none of which has occured
# -3.0 is for the pixel to geographic units in the y-direction, N-S
# 841198.5, This represents the coordinate of the top left within the raster


print('2017 Meta Data :', DEM_2017.meta) 

print('2017 DEM bounds : ', DEM_2017.bounds)

print('2017 DEM transform : ', DEM_2017.transform)


#show(DEM_2009)

#show(DEM_2017)
# can show if want to 


#%%





# Define the nodata value (replace -9999 with the actual nodata value)
nodata_value_2017 = -9999
nodata_value_2009 = -3.4028234663852886e+38

# Setting nodata values to NaN
Array_2009_fixed = np.where(Array_2009 == nodata_value_2009, np.nan, Array_2009)
Array_2017_fixed = np.where(Array_2017 == nodata_value_2017, np.nan, Array_2017)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))  

# Plot the cropped images on the subplots
im1 = ax1.imshow(Array_2009_fixed.squeeze()) # Squeeze removes the unnessecary band axis (band , x ,y). Now the array is 2d
im2 = ax2.imshow(Array_2017_fixed.squeeze())

# Add colorbars to each subplot
cbar1 = fig.colorbar(im1, ax=ax1)
cbar2 = fig.colorbar(im2, ax=ax2)

ax1.set_title('2009 DEM ')
ax2.set_title('2017 DEM ')

plt.show()






#%%



# histograms of Raw Array with 'nodata' values


# Create a single figure with one subplot
fig, ax = plt.subplots(figsize=(10, 5))

# Plot the histogram for the 2009 dataset
show_hist(Array_2009, bins=35, lw=0.0, stacked=False, alpha=0.3, histtype='stepfilled', ax=ax, title="Elevation Histograms")
# Plot the histogram for the 2017 dataset
show_hist(Array_2017, bins=25, lw=0.0, stacked=False, alpha=0.3, histtype='stepfilled', ax=ax)

# Add a legend
ax.legend(["2009", "2017"])

plt.show()




#%%




# When The 'nodata' values are set to NaN



# Create a single figure with one subplot
fig, ax = plt.subplots(figsize=(10, 5))

# Plot the histogram for the 2009 dataset
show_hist(Array_2009_fixed, bins=35, lw=0.0, stacked=False, alpha=0.3, histtype='stepfilled', ax=ax, title="Elevation Histograms")
# Plot the histogram for the 2017 dataset
show_hist(Array_2017_fixed, bins=25, lw=0.0, stacked=False, alpha=0.3, histtype='stepfilled', ax=ax)

# Add a legend
ax.legend(["2009", "2017"])

plt.show()






#%%


# Creating a Reprojection, if it doesn't already exist




# Path to the input raster file
input_raster = 'w001001.tif'

# Path to the output reprojected raster file
output_raster = 'w001001_reproj.tif'

# Check if the output raster file already exists
if not os.path.exists(output_raster):
    # If the output raster file does not exist, proceed with the reprojection
    with rio.open(input_raster) as src:
        dst_crs = DEM_2017.crs  # Define the target CRS
        transform, width, height = calculate_default_transform( # Defining three meta varibales as a product of the transform
            src.crs, dst_crs, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({ # Updating the meta variables
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        # Open the destination file for writing
        with rio.open(output_raster, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                # Reproject each band from the source to the destination dataset
                reproject(
                    source=rio.band(src, i),
                    destination=rio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest)
        print('File saved at : ' , str(output_raster))
else:
    print("Output raster file already exists. Skipping reprojection.")





#%%




# Take a Look at the reprojected data

# File path of the reprojected image
reprojected_image_path = 'w001001_reproj.tif'

# Open the reprojected image file
with rio.open(reprojected_image_path) as reprojected_image:
    # Display the reprojected image
    show(reprojected_image, title='Reprojected Image')
    reprojected_image.close()





#%%



# Now Converting from Feet to meters




if not os.path.exists('reprojected_dem_meters.tif'):
    with rio.open(reprojected_image_path) as src:
        # Read the raster data
        data = src.read()
        # Get the metadata
        kwargs = src.meta.copy()

    # Convert the raster data from feet to meters
    data_meters = data * 0.3048 # Note this is also applied to the 'nodata' values

    # Update the dtype in metadata to float32 since multiplying by a float will result in a float raster
    kwargs['dtype'] = 'float32'

    # Update the units in metadata
    kwargs['units'] = 'meters'

    # Write the converted raster data to a new file
    with rio.open('C:/Users/jettr/Dropbox (University of Oregon)/ESP_Research/Python Files/reprojected_dem_meters.tif', 'w', **kwargs) as dst:
        dst.write(data_meters)

    print("Reprojected DEM converted from feet to meters and saved as reprojected_dem_meters.tif")
else:
    print("Output raster file already exists. Skipping Conversion.")



#%%



# Visualize the Reprojected  2009 DEM also in meters



DEM_2009_Reproj_meters = rio.open('reprojected_dem_meters.tif')

nodata_value_2009 = -3.4028234663852886e+38 * 0.3048 # Nodata value was changed by the ft to meters conversion

DEM_2009_Repoj_metes_data = DEM_2009_Reproj_meters.read()

# Replace nodata values with NaN
Reproject_Array_2009_fixed = np.where(DEM_2009_Repoj_metes_data == nodata_value_2009, np.nan, DEM_2009_Repoj_metes_data)

plt.imshow(Reproject_Array_2009_fixed.squeeze())
plt.colorbar()
plt.show()




#%%



# We Know that we want to clip the 2009 DEm to fit the extents of the 2017 DEM, Lete's get an idea of what that might look like


Clipped_2009 = Reproject_Array_2009_fixed[:, 8000:12000 , 4000 : 9000 ] # Slicing the Array For dimensions we want

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))  


# Plot the cropped images on the subplots
im1 = ax1.imshow(Clipped_2009.squeeze()) # Squeeze removes the unnessecary band axis (band , x ,y). Now the array is 2d
im2 = ax2.imshow(Array_2017_fixed.squeeze())

# Add colorbars to each subplot
cbar1 = fig.colorbar(im1, ax=ax1)
cbar2 = fig.colorbar(im2, ax=ax2)

ax1.set_title('2009 DEM ')
ax2.set_title('2017 DEM ')

plt.show()

# Looking at this, we can't really tell how well how DEM's match up. SO , 
# something that we may want to do, is to first find the shape of the 2017 DEM. This will have the width,
# height, and all other characters that we want to georeference to. So we want to first make the 2009 raster
# the same size and shape as the 2017 raster. Then , to make sure they are lined up, we want to get
# the coordinates of the top right and bottom left corners of the 2017 DEM, in both the xy and the CRS.
# then we want to give those values to the 2009 DEM. This will make the 2009 DEM, the same size, shape and 
# location.




#%%


# Let's check some of the meta data, as well as look at their transforms. This will tell us how the rows, cols are related
# to the crs x,y coordinates




path2017 = 'output_be.tif'
with rio.open(path2017) as src:
    print('For the 2017 DEM')
    print(src.meta)
    print(src.transform)
    print(src.xy(0,0)) # Find (Row,Col) and returns (x,y)
    print()
    src.close()

#Transform = Affine(1.0, 0.0, 412794.5, 0.0, -1.0, 4864846.5)
#transformer = rio.transform.AffineTransformer(Transform)
#transformer.xy(0,0) # (412795.0, 4864846.0)


path2009 = 'reprojected_dem_meters.tif'

with rio.open(path2009) as src:
    print('For the 2009 DEM')
    print(src.meta)
    print(src.transform)
    print(src.xy(0,0)) # Find (Row,Col) and returns (x,y)
    src.close()





#%%



# Masking the 2009 DEM to fit the extents of the 2017 DEM

# We want to put on a mask over the 2009 DEM. 
# Here we are checking to first make sure the Files have not been created already
# Then we open the 2017 file, get the bounds and make it a Polygon. then open the 2009 file, and apply a mask that is the shape
# of the polygon, cropping out everythin outside the polygon. Then we update the metadata to this new cropped image/array, and write
# out the file to our output path. 




from shapely.geometry import box

# Paths to your DEMs
path2017 = 'output_be.tif'
path2009 = 'reprojected_dem_meters.tif'

output_path = 'DEM2009_cropped.tif'

# Check if the output file directory exists
if not os.path.exists(output_path):
    # Open the 2017 DEM to get its extent
    with rio.open(path2017) as src2017:
        # Read the extent of the 2017 DEM
        extent_2017 = src2017.bounds
        nodata_value_2017 = src2017.nodata

        # Convert the extent to a polygon geometry
        extent_polygon = box(*extent_2017)

        # Open the 2009 DEM and crop it to match the extent of the 2017 DEM
        with rio.open(path2009) as src2009:
            # Crop the 2009 DEM based on the extent of the 2017 DEM
            cropped_data, cropped_transform = mask(src2009, [extent_polygon], crop=True)

            # Update metadata
            cropped_meta = src2009.meta.copy()
            cropped_meta.update({
                'driver': 'GTiff',
                'height': cropped_data.shape[1],
                'width': cropped_data.shape[2],
                'transform': cropped_transform,
                'nodata': nodata_value_2017
            })

            # Write the cropped DEM to a new raster file
            with rio.open(output_path, 'w', **cropped_meta) as dst:
                dst.write(cropped_data)
else:
    print("File already exists. Skipping cropping.")







#%%



# Taking a look at the new Cropped 2009 DEM and the 2017 DEM 

DEM_2009_cropped = rio.open(output_path)

nodata_value_2009 = -3.4028234663852886e+38


Array_cropped = DEM_2009_cropped.read()
Array_cropped_nodata_fix = np.where(Array_cropped == nodata_value_2009 , np.nan , Array_cropped)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), sharey=True, sharex=True)

# Plot the cropped images on the subplots
im1 = ax1.imshow(Array_cropped_nodata_fix.squeeze(), cmap='viridis')  # Squeeze removes the unnecessary band axis (band , x ,y). Now the array is 2d
im2 = ax2.imshow(Array_2017_fixed.squeeze(), cmap='viridis')

cbar = fig.colorbar(im2, ax=[ax1, ax2], orientation='vertical', shrink=0.6)


ax1.set_title('2009 DEM ')
ax2.set_title('2017 DEM ')

plt.show()



#%%

path2017 = 'output_be.tif'
path2009 = 'DEM2009_cropped.tif'


with rio.open(path2017) as src:
    print('For the 2017 DEM')
    print(src.meta)
    print(src.transform)
    print(src.xy(0,0)) # Find (Row,Col) and returns (x,y)
    print()
    src.close()

#Transform = Affine(1.0, 0.0, 412794.5, 0.0, -1.0, 4864846.5)
#transformer = rio.transform.AffineTransformer(Transform)
#transformer.xy(0,0) # (412795.0, 4864846.0)


with rio.open(path2009) as src:
    print('For the 2009 DEM')
    print(src.meta)
    print(src.transform)
    print(src.xy(0,0)) # Find (Row,Col) and returns (x,y)
    src.close()

#%%

