#!/usr/bin/env python


import subprocess
import numpy as np 
from osgeo import gdal 
from osgeo.gdalnumeric import *  
from osgeo.gdalconst import *

def gdal_build_vrt(name,liste): 
	""" Make a virtual mosaic from all TIFF files contained in list.txt
	"""
	out_file = name + '.vrt'
	command = ['gdalbuildvrt -input_file_list' + ' ' + liste + ' ' + out_file]
	subprocess.call(command,shell=True) 

	return out_file







if __name__ == '__main__' : 

	directory = 'Hawaii_30'
	name = 'Hawaii_30'


