#!/usr/bin/env python
import subprocess


def get_aspect(input_dem): 
	""" Returns an aspect map 
	Each pixel has a value [0-360] indicating azimuth 
	"""
	out_file = input_dem.split('.')[0] + '_aspect.tif'
	command = ['gdaldem aspect' + ' ' + input_dem + ' ' + out_file]
	subprocess.call(command,shell=True) 

	return out_file


def get_slope(input_dem): 
	""" Returns a slope map 
	Each pixel has a value in degree of the local slope
	"""
	out_file = input_dem.split('.')[0] + '_slope.tif'
	command = ['gdaldem slope' + ' ' + input_dem + ' ' + out_file]
	subprocess.call(command,shell=True) 

	return out_file

""" Good to keep in mind : 
-alg ZevenbergenThorne:
(GDAL >= 1.8.0) Use Zevenbergen & Thorne formula, instead of Horn's formula, to compute slope & aspect. 
The literature suggests Zevenbergen & Thorne to be more suited to smooth landscapes, 
whereas Horn's formula to perform better on rougher terrain.
"""