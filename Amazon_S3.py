
"""

GET ELEVATION DATA FROM AMAZON S3

"""

import subprocess 

def get_files(N,E,region): 

	# Empty list 
	files = []
	# New folder 
	subprocess.call('mkdir {}'.format(region),shell=True)

	
	for n in N: 
		for e in E: 
			# Downloading data 
			command = ['s3cmd get s3://srtm-30.openterrain.org/source/N{n}_E{e}_1arc_v3_bil.zip {reg}/{reg}_{n}_{e}.zip'.format(n=n,e=e,reg=region)]
			subprocess.call(command,shell=True) 

			# Unzip data in the same folder 
			command = 'unzip {reg}/{reg}_{n}_{e}.zip -d {reg}/'.format(n=n,e=e,reg=region)
			print command
			subprocess.call(command,shell=True)

			# Delete the .zip file 
			subprocess.call('rm {reg}/{reg}_{n}_{e}.zip'.format(n=n,e=e,reg=region),shell=True)

			# DEM files 
			file = '{reg}/n{n}_e{e}_1arc_v3.bil'.format(n=n,e=e,reg=region)
			files.append(file)

	return files 

if __name__ == '__main__' : 


	region = 'Switzerland'
	N = ['46','47']
	E = ['006','007','008','009']

	files = get_files(N,E,region)
	print files 
