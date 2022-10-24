#!/bin/sh
#SBATCH -J eIBI_N4
#SBATCH -N 1
#SBATCH --exclusive
#SBATCH --no-requeue
#SBATCH --time=00:30:00

methodlist="remapbil remapbic remapnn remapdis remapycon remapcon remapcon2 remaplaf"
methodlist="remapbil"
pathin='/data/vdi/tbrivoal/TILES_EMODNET/'
pathout="/data/vdi/tbrivoal/"
grid='/data/vdi/tbrivoal/INPUT/emodnet.grid'
echo $pathout
# loop on tiles
for fic in `ls ${pathin}/??_2018.nc`; do
  echo ===
  echo start: `date`
  echo $fic
  ficnum=`basename $fic | cut -d '_' -f1`
  ficout=${pathin}/${ficnum}_2018.nc
  echo $ficout
  for method in ${methodlist}; do
    echo $method ...
    pathmethod="${pathout}/nc_${method}"
    mkdir -p $pathmethod
    ficout_interp=${pathmethod}/EMODNET_${ficnum}_2018.nc
    if [ -f $ficout_interp ]; then
    echo "FILE $ficout_interp exists, next"
    else
     
    cdo ${method},${grid} $ficout ${ficout_interp}
    fi
  done
  echo end: `date`
done
