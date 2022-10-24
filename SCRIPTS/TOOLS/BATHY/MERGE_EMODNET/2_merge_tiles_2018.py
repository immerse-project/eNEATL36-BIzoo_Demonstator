# coding: utf-8
import sys
import numpy as np
#sys.path.append('/home/karen/workspace/Utils/Python')
#from skimage import measure
import xarray as xr
import scipy as sp
from scipy.io import netcdf
import os
import math 
import scipy.ndimage
from shutil import copyfile
from netCDF4 import Dataset

########### Main  ###########
# Define the paths
tiles = ['C2', 'C3', 'C4', 'C5', 'D2', 'D3', 'D4', 'D5','E2', 'E3', 'E4', 'E5','F2','F3','F4','F5','F6','G2', 'G3']
datapath  = '/scratch/work/brivoalt/MAKE_EMODNET/nc_remapbil/'
outpath  = datapath

# Loop on all tiles
for tile in tiles:
    print('%s ...' % (tile))
    
    ## Read file and get depth_smooth
    infile = datapath+'EMODNET_'+tile+'_2018.nc'

    print(infile)
    infile_xr = xr.open_dataset(infile)

    depth_smooth = infile_xr.DEPTH.values
    if tiles[0] == tile:
        ### If first occurence of the loop, initialize bathy
        print('Initialize bathy ...')
        bathy = np.zeros_like(depth_smooth) #-1.e+34
        lonmod = infile_xr.lon.values 
        latmod = infile_xr.lat.values
    ## Append bathy with the tile 
    bathy = np.where(xr.ufuncs.isnan(depth_smooth) == True ,bathy, depth_smooth*-1)
    
    ## Write
    outfile = outpath+'bathy_merge_EMODNET_'+tile+'.nc'
    f = netcdf.netcdf_file(outfile, 'w')
    f.createDimension('lon',lonmod.shape[0])
    f.createDimension('lat',latmod.shape[0])

    depth = f.createVariable('depth','d',('lat','lon',))
    depth[:,:] = bathy
    depth._fill_value = float(1.e+34)
    f.close()

bathy = np.where(bathy < 0 ,0 , bathy)

## Write a nedcdf file similar to the input bathymetry
outfile = outpath+'bathy_emodnet_on_EMODNET_2018.nc'
copyfile(infile,outfile)
f = Dataset(outfile, 'a')
#bathymetry = f.createVariable('bathymetry','f8',('y','x',),fill_value=0)
bathymetry = f.createVariable('bathymetry','f8',('lat','lon',),fill_value=float(1.e+34))
bathymetry[:] = bathy
f.close()
