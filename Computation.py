#!/usr/bin/env python

"""

SOLUTION 3 : Local aspect weight calculation 
IDEA : An initial hill-shaded image is
generated by applying a north-west light direction and is partly replaced by the enhanced
weighted combination of the shading images derived from certain other lighting directions,
where the amount of partial replacement depends on the incident angle. This methodology
aims to achieve a more balanced result of hill-shading, in such a way that the perception of
the initial optimal lighting is preserved, as well as, the major relief forms in all directions
are revealed or even sharper local details are enhanced. 
Source : http://www.mountaincartography.org/publications/papers/ica_cmc_sessions/5_Moscow_Session_Mountain_Carto/moscow_loisios.pdf

"""
# Imports 
import subprocess 
import os 
import numpy as np 
import numpy.ma as ma
from osgeo import gdal 
from osgeo.gdalnumeric import *  
from osgeo.gdalconst import *

# Local imports 
from Aspect import get_aspect, get_slope
from PreProcessing import Reproject, raster_to_numpy, get_no_data_value, get_smoother
import HillShade 

def Computation(region,north,east): 

	# Global variables 
	azimuths = [225,270,315,360] 
	angle = 45
	rasterBand = 1 # Both for Aspect and Slope files 
	path = '{reg}/n{n}_e{e}_1arc_v3.bil'.format(reg=region,n=north,e=east)
	file = Reproject(path,'{}_{}'.format(north,east),region) 
	
	# Use of gdaldem to get slope and aspect raster files 
	aspectFile = get_aspect(file)
	slopeFile = get_slope(file) 

	# Computing of the hillshading files - no_data has an output value of 0 (black pixel)
	hillshadedFiles = HillShade.hillshade(file,azimuths,angle)

	# Reading Metadatas to compute the output file at the end 
	dataset_in = gdal.Open(file,GA_ReadOnly)
	band_in = dataset_in.GetRasterBand(rasterBand)

	# Reading the aspect raster file as a numpy array - aspect_m.mask corresponds to no_data
	aspect = raster_to_numpy(aspectFile)
	aspect_m = ma.masked_values(aspect,get_no_data_value(aspectFile)) 
	aspect[aspect_m.mask] = 0 # no_data values put to 0 (same than -zero_for_flat)

	# Computation of local weight numpy arrays 
	sum_array = np.zeros(aspect.shape)
	for i,e in enumerate(azimuths): 
		weight = (np.cos(np.radians(aspect-e)) + 1) / 2 # Each pixel has a value between 0 and 1 
		hillshade = raster_to_numpy(hillshadedFiles[i])
		weightedFile = weight * hillshade # This is not a matrix operation 
		sum_array += weightedFile

	# Multi-directional light source array 
	md_array = sum_array / 4 

	# Initial Hillshaded file - 315 degree azimuth with 30 degree elevation is considered the "natural way" 
	Hillshade_initial = hillshadedFiles[2]
	initial_array = raster_to_numpy(Hillshade_initial)

	# Computing local incidents angles raster I
	slope = raster_to_numpy(slopeFile)
	slope_m = ma.masked_values(slope,get_no_data_value(slopeFile)) # slope_m.mask corresponds to no_data
	slope[slope_m.mask] = 0 # no_data values put to 0

	initial_az = 315 
	initial_alt = angle
	I = math.cos(math.radians(initial_alt))*np.sin(np.radians(slope))*np.cos(np.radians(aspect-initial_az)) + math.sin(math.radians(initial_alt))*np.cos(np.radians(slope))
	Blender = np.sin(I) * np.sin(I)

	# Merging the initial hillshading and the multi-directionnal hillshading 
	# In this way, the closer to 90deg the incident angle gets, the more dominant is the role of
	# multi-directional hill-shading in the final image.
	Final = Blender*md_array + (1-Blender)*initial_array

	# Explicitely -10000 value for no_data 
	value = -10000
	Final[aspect_m.mask] = value
	Final[slope_m.mask] = value

	# Generation of the output file 
	outfile = '{reg}/Solution_{reg}_{n}_{e}.tif'.format(reg=region,n=north,e=east)
	driver = gdal.GetDriverByName('GTiff')
	dataset_out = driver.Create(outfile,dataset_in.RasterXSize, dataset_in.RasterYSize, 1, band_in.DataType)
	CopyDatasetInfo(dataset_in,dataset_out) # Copy all the MetaData's (info, projection geotransform, etc..) 
	band_out = dataset_out.GetRasterBand(1)
	band_out.SetNoDataValue(value)
	BandWriteArray(band_out, Final)

	# Close the datasets
	band_in = None 
	dataset_in = None 
	band_out = None 
	dataset_out = None 

	# Delete files generated during the process 
	os.remove(file)
	os.remove(aspectFile)
	os.remove(slopeFile) 
	for el in hillshadedFiles: 
		os.remove(el)

	return outfile


if __name__ == '__main__': 

	sol = Solution3('Switzerland','46','006')



