#!/bin/sh
#SBATCH -J RNFtool
#SBATCH -N 1
#SBATCH --exclusive
#SBATCH --no-requeue
#SBATCH --time=00:20:00
#SBATCH --account=cmems

DO_MOTHER=true
DO_CHILD=false
IS_NOT_RIVERS=false
DOMCFG_IN=/scratch/work/brivoalt/MAKE_DOMAINcfg/eNEATL36_AGRIF_emodNET2018_finaldomain_corrected_with_FES2014/domain_cfg_init.nc
DOMCFG_IN_ZOOM=/scratch/work/brivoalt/MAKE_DOMAINcfg/eNEATL36_AGRIF_emodNET2018_finaldomain_corrected_with_FES2014/1_domain_cfg.nc

RNF_IN=/scratch/work/brivoalt/MAKE_RUNOFFS/INPUTS/runoff_eNEATL36_CLIM_y2018.nc
RNF_OUT_MOTHER=/scratch/work/brivoalt/MAKE_RUNOFFS/OUT/runoff_eNEATL36_CLIM_y2018_emodnet.nc
RNF_OUT_ZOOM=/scratch/work/brivoalt/MAKE_RUNOFFS/OUT/1_runoff_eNEATL36_CLIM_y2018_tmp.nc

LVERB=False

RNFTOOL_DIR=/home/ext/mr/smer/brivoalt/TOOLS/RNFTOOL/
if $DO_MOTHER
then
    sed -e "s%DOMCFG_IN%`echo $DOMCFG_IN`%g" \
        -e "s%RNF_IN%`echo $RNF_IN`%g" \
        -e "s%RNF_OUT_MOTHER%`echo $RNF_OUT_MOTHER`%g" \
        -e "s%LVERB%`echo $LVERB`%g" ${RNFTOOL_DIR}/extrap_near_coasts.py > extrap_near_coasts.py.work
    python extrap_near_coasts.py.work
echo "DONE"
fi

# Note: here we treat differently the rivers and the climatology. But they can also be treated together 
# (It was more convenient to have the rivers in a separate file to check if everything was OK)
if $DO_CHILD
then
    if $IS_NOT_RIVERS
    then
        sed -e "s%DOMCFG_IN_ZOOM%`echo $DOMCFG_IN_ZOOM`%g" \
            -e "s%DOMCFG_IN%`echo $DOMCFG_IN`%g" \
            -e "s%RNF_OUT_MOTHER%`echo $RNF_OUT_MOTHER`%g" \
            -e "s%RNF_OUT_ZOOM%`echo $RNF_OUT_ZOOM`%g" \
            -e "s%LVERB%`echo $LVERB`%g" ${RNFTOOL_DIR}/place_on_child_grid.py.clim > place_on_child_grid.py.clim.work
        python place_on_child_grid.py.clim.work
        echo "DONE"
    else
       # IF rivers, the center of the river mouth is scrictly placed on the parent river point
       sed -e "s%DOMCFG_IN_ZOOM%`echo $DOMCFG_IN_ZOOM`%g" \
            -e "s%DOMCFG_IN%`echo $DOMCFG_IN`%g" \
            -e "s%RNF_OUT_MOTHER%`echo $RNF_OUT_MOTHER`%g" \
            -e "s%RNF_OUT_ZOOM%`echo $RNF_OUT_ZOOM`%g" \
            -e "s%LVERB%`echo $LVERB`%g" ${RNFTOOL_DIR}/place_on_child_grid.py.riv > place_on_child_grid.py.riv.work
        python place_on_child_grid.py.riv.work
        echo "DONE"
   fi
fi

