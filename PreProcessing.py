#!/usr/bin/env python

import subprocess
import numpy as np 
from osgeo import gdal 
from osgeo.gdalnumeric import *  
from osgeo.gdalconst import *

# ----------------------------------------------------------------------------------------------------
# These functions are called once at the beginning in order to provide files to work with
# ----------------------------------------------------------------------------------------------------


def translate_to_tif(input_file,output_file): 
	""" Returns a .tif file named 'output_file'
	Takes a DEM Gdal-compatible file 'input'
	(in order to use gdaldem for the hillshading)
	"""
	new_file = output_file + '.tif'
	command = ['gdal_translate -of GTiff' + ' ' + input_file + ' ' + new_file]
	subprocess.call(command,shell=True)

	return new_file


def Reproject(input_file,output_file,region): 
	""" Returns a projection with several options
	Reproject to Spherical Mercator EPSG:3857 (Most DEM files are provided in Plate Carree projection)
	Output band data should be float type : -ot Float32  
	Source : http://www.gdal.org/gdalwarp.html
	"""
	base = 'gdalwarp' 
	no_data = '-dstnodata -10000'
	resampling = '-r lanczos'
	data_type = '-ot Float32'
	tiled = '-co \"TILED=YES\"'
	zlevel = '-co \"ZLEVEL=1\"'
	tfw = '-co \"TFW=NO\"'
	projection = '-t_srs EPSG:3857'# To Spherical Mercator in this case 
	overwrite = '-overwrite'
	output = region + '/' + output_file +'.tif'

	command = ' '.join([base,no_data,data_type,tiled,zlevel,tfw,overwrite,resampling,projection,input_file,output])
	subprocess.call(command,shell=True) 

	return output


def raster_to_numpy(fileName): 
	""" Returns a numpy array from a raster file 
	"""
	
	rasterBand = 1
	dataset = gdal.Open(fileName,GA_ReadOnly)
	band = dataset.GetRasterBand(rasterBand)
	data = band.ReadAsArray() # Read them as a numpy array

	dataset = None 
	band = None 
	
	return data 



