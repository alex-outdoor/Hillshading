#!/usr/bin/env python


import subprocess


def hillshade(input,array,alt): 
	""" Returns n file(s) hillshaded (based on the input)
	from a certain azimuth (item(s) in array)
	"""
	files = []
	if type(array) == list: 	
		for i, az in enumerate(array): 
			new_file = input.split('.')[0] + '_{}_{}'.format(az,alt) + '.tif'
			command = ['gdaldem hillshade -az {} -alt {}'.format(az,alt) + 
						' ' + input + ' ' + new_file]
			subprocess.call(command,shell=True)
			files.append(new_file)

		return files

	else: 
		raise TypeError("Array (second input fonction) must be a list")

