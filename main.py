#!/usr/bin/env python

"""

MAIN file 

"""

# Imports 
import math
import numpy as np 
import numpy.ma as ma

# Local imports 
from Amazon_S3 import get_files 
from Solution3 import Solution3 
from PostProcessing import gdal_build_vrt 

# Main variables 
region = 'Belgium'
N = ['50']
E = ['002']

# Getting the DEM files (format .bil)
files = get_files(N,E,region)

# Actual computation 
result = []
for n in N: 
	for e in E: 
		solution = Solution3(region,n,e)
		result.append(solution)

# Merging the tiles result files together 
liste = '{reg}/list.txt'.format(reg=region)
with open(liste,'wb') as out: 
	for el in result: 
		out.write(el + '\n')

final = gdal_build_vrt('{reg}/Assembly_{reg}'.format(reg=region),liste)




