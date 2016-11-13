# from datetime import date, datetime, timedelta
# tiles = ['h09v04','h10v04']
 
from datetime import date, datetime, timedelta
import subprocess
from subprocess import call
import os
import glob

def genDates(start, end, delta):
	curr = start
	while curr < end:
		yield curr
		curr += delta

port='ftp://n5eil01u.ecs.nsidc.org/SAN/MOSA/MYD10A1.005/'
grid=['h08v05']


# if os.path.isdir("MODIS"):
# 	print 'MODIS directory exists'
# 	os.chdir("MODIS")

# else: 
# 	print 'creating directory MODIS'
# 	os.mkdir("MODIS")
# 	os.chdir("MODIS")

for cell in grid:
	os.mkdir(cell)
	os.chdir(cell)

	for result in genDates(date(2013, 4, 3), date(2016, 7, 8), timedelta(days=1)):
		cmd = "curl -l ftp://n5eil01u.ecs.nsidc.org/SAN/MOSA/MYD10A1.005/"+result.strftime("%Y.%m.%d")+"/ | grep -E "+cell+".*hdf$" 
		output = subprocess.Popen([cmd], shell =True, stdout=subprocess.PIPE).communicate()[0]
		# dlist.append({result.strftime("%Y.%m.%d"):output})
		for i in output.split():
			cmd = "curl -O ftp://n5eil01u.ecs.nsidc.org/SAN/MOSA/MYD10A1.005/"+result.strftime("%Y.%m.%d")+'/'+i
			call([cmd], shell=True)

		call([command], shell =True)

	print "converting to .tiff..."

	for i in glob.glob("*.hdf"):
		cmd = 'gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'+"'"+str(i)+"'"+':MOD_Grid_Snow_500m:Fractional_Snow_Cover '+ i.split(".hdf")[0] +'.tiff'
		call([cmd], shell=True)

	os.chdir("..")


def merge_reproj():
	os.mkdir("merger")
	mlist = [glob.glob(x+"/*tiff") for x in grid]
	for i,j in zip(mlist[0],mlist[1]):
		outfile = i.split(".")[1] + "." + j.split(".")[2] + "." + i.split(".")[2] + '-merger.tiff '
		cmd = 'gdal_merge.py -o ' + "merger/"+outfile + i + ' ' + j
 		call([cmd], shell =True)
 	
 	os.chdir("merger")	
	for r in glob.glob("*.tiff"):
		cmd = "gdalwarp -t_srs '+proj=utm +zone=11 +datum=WGS84' "+r+" "+"WGS84."+r

		call([cmd], shell=True)	
	

merge_reproj()





# gdalwarp -cutline ../idaho.shp -crop_to_cutline -dstalpha MYD10A1.A2011009.h10v04.005.2011012001553.tiff clipped_MYD10A1.A2011009.h10v04.005.2011012001553.tiff 



# with open('list.txt', 'r') as f:
# 	for line in f:
# 		print lin