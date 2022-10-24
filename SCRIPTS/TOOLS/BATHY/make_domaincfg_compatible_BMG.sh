#!/bin/sh

DOMCFG=$1
OUTFILE=$2
OUTFILE_BATHY=$3
cp $DOMCFG tmp.nc
ncrename -d time_counter,t tmp.nc 
ncrename -d nav_lev,z tmp.nc
ncrename -v bathy_metry,Bathymetry tmp.nc

ncap2 -O -s 'Bathymetry=float(Bathymetry)' tmp.nc tmp2.nc
mv tmp2.nc tmp.nc

ncks -C -O -x -v x,y tmp.nc $OUTFILE
rm tmp.nc
ncks -v glamt $OUTFILE glamt
ncks -v gphit $OUTFILE gphit
ncks -v Bathymetry $OUTFILE tmp.nc
ncks -A glamt tmp.nc 
ncks -A gphit tmp.nc
ncks -3 tmp.nc tmp2.nc
mv tmp2.nc $OUTFILE_BATHY
rm tmp.nc -f
