#!/bin/sh

DOMCFG_in=$1
bathy=$2
DOMCFG_out=$3

# rename variable in bathymetry file
ncrename -d t,time_counter $bathy 
ncrename -v Bathymetry,bathy_metry $bathy 


# Add bathymetry in domain_cfg file 
ncks -C -O -x -v bathy_metry $DOMCFG_in $DOMCFG_out
ncks -A $bathy $DOMCFG_out 
# End

