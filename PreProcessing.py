#!/usr/bin/env python

import subprocess
import numpy as np 
from osgeo import gdal 
from osgeo.gdalnumeric import *  
from osgeo.gdalconst import *

# ----------------------------------------------------------------------------------------------------
# These functions are called once at the beginning in order to provide files to work with
# ----------------------------------------------------------------------------------------------------

def Reproject(input_file,output_file,region,res=None,size=None): 
	""" Returns a projection with several options
	Reproject to Spherical Mercator EPSG:3857 (Most DEM files are provided in Plate Carree projection)
	Output band data should be float type : -ot Float32  
	Source : http://www.gdal.org/gdalwarp.html
	"""
	
	base = 'gdalwarp' 
	no_data = '-dstnodata -10000'
	resampling = '-r lanczos'
	data_type = '-ot Float32'
	tiled = '-co "TILED=YES"'
	zlevel = '-co "ZLEVEL=1"'
	tfw = '-co "TFW=NO"'
	projection = '-t_srs EPSG:3857'# To Spherical Mercator in this case 
	overwrite = '-overwrite'
	

	if res == None and size == None: 
		output = region + '/' + output_file +'.tif'
		command = ' '.join([base,no_data,data_type,tiled,zlevel,tfw,overwrite,resampling,projection,input_file,output])
	if res != None: 
		Resolution = '-tr {} {}'.format(res[0],res[1])
		output = region + '/' + output_file + '_res_{}_{}'.format(res[0],res[1]) +'.tif'
		command = ' '.join([base,Resolution,overwrite,resampling,input_file,output])
	if size!=None: 
		Size = '-ts {} {}'.format(size[0],size[1])
		output = region + '/' + output_file + '_size_{}_{}'.format(size[0],size[1]) +'.tif'
		command = ' '.join([base,Size,overwrite,resampling,input_file,output])

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


def get_no_data_value(file): 
	""" Return the no_data value from a raster file """

	rasterBand = 1 
	dataset = gdal.Open(file,GA_ReadOnly)
	band = dataset.GetRasterBand(rasterBand)
	no_data_value = band.GetNoDataValue()
	dataset = None
	band = None
	
	return no_data_value


def get_smoother(file,region): 
	""" Return a smoother version of the input file
	This has been tried just before computing the aspect file but gives
	really bad results especially all around lakes and flat areas where a 
	lot of interpolation occurs
	"""

	rasterBand = 1 
	dataset = gdal.Open(file,GA_ReadOnly)
	info = dataset.GetGeoTransform()
	original_res = [info[1],info[5]] 
	original_size = [dataset.RasterXSize,dataset.RasterYSize]
	fact = 10

	low_res = Reproject(file,'low_res_file',region,res=[fact*info[1],fact*info[5]])
	high_res = Reproject(low_res,'high_res_file',region,size=original_size) # If using original resolution, getting not exactly the same size 

	return high_res 

if __name__ == '__main__': 

	path = 'Switzerland/n46_e006_1arc_v3.bil'
	file = Reproject(path,'test','Switzerland')
	get_smoother(file,'Switzerland')








