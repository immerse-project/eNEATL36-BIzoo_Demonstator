#!/bin/sh
#SBATCH -J rebuild
#SBATCH -N 1
#SBATCH --exclusive
#SBATCH --no-requeue
#SBATCH --time=08:00:00
#SBATCH --account=cmems
# Comm/Fabric
# -----------
export DAPL_ACK_RETRY=7
export DAPL_ACK_TIMER=20
export DAPL_IB_SL=0
export DAPL_UCM_CQ_SIZE=8192
export DAPL_UCM_DREQ_RETRY=4
export DAPL_UCM_QP_SIZE=8192
export DAPL_UCM_REP_TIME=8000
export DAPL_UCM_RTU_TIME=8000
export DAPL_UCM_WAIT_TIME=10000
export I_MPI_CHECK_DAPL_PROVIDER_COMPATIBILITY=0
export I_MPI_CHECK_DAPL_PROVIDER_MISMATCH=none
export I_MPI_DAPL_RDMA_MIXED=enable
export I_MPI_DAPL_SCALABLE_PROGRESS=1
export I_MPI_DAPL_TRANSLATION_CACHE=1
export I_MPI_DAPL_UD_DIRECT_COPY_THRESHOLD=65536
export I_MPI_DAPL_UD=on
export I_MPI_FABRICS=shm:dapl
export I_MPI_DAPL_PROVIDER=ofa-v2-mlx5_0-1u
export I_MPI_FALLBACK=disable
export I_MPI_FALLBACK_DEVICE=disable
export I_MPI_DYNAMIC_CONNECTION=1
export I_MPI_FAST_COLLECTIVES=1
export I_MPI_LARGE_SCALE_THRESHOLD=8192
# File system
# -----------
export I_MPI_EXTRA_FILESYSTEM_LIST=lustre
export I_MPI_EXTRA_FILESYSTEM=on
# Slurm
# -----
export I_MPI_HYDRA_BOOTSTRAP=slurm
export I_MPI_SLURM_EXT=0
# Force kill job
# --------------
export I_MPI_JOB_SIGNAL_PROPAGATION=on
export I_MPI_JOB_ABORT_SIGNAL=9
# Extra
# -----
export I_MPI_LIBRARY_KIND=release_mt
export EC_MPI_ATEXIT=0
export EC_PROFILE_HEAP=0
# Process placement (cyclic)
# --------------------------
export I_MPI_JOB_RESPECT_PROCESS_PLACEMENT=off
export I_MPI_PERHOST=1
# Process pinning
# ---------------
export I_MPI_PIN=enable
export I_MPI_PIN_PROCESSOR_LIST="allcores:map=scatter" # map=spread
# -------------------------------------------------------
# Indispensable
# -------------------------------------------------------
ulimit -Sl unlimited
ulimit -St unlimited
ulimit -Ss unlimited
ulimit -S  unlimited

ulimit -c 0
ulimit -s unlimited
export FORT_BUFFERED=true

# -------------------------------------------------------
# Chargement des differents modules
# -------------------------------------------------------
#. /home/ext/mr/smer/pianezzej/SAVE/env/env_frc_nemo.sh
module purge

module load intel/2018.5.274
module load intelmpi/2018.5.274

module load phdf5/1.8.18
module load netcdf_par/4.7.1_V2
module load xios-2.5_rev1903

module load netcdf-c/4.7.1_V2
module load netcdf-fortran/4.5.2_V2

export NETCDF_CONFIG=$NETCDFF_BIN/nf-config

export NEMOCONF_DIR=/home/ext/mr/smer/brivoalt/NEMO4/r4.0-HEAD/cfgs

PATH="/home/ext/mr/smer/soniv/perl5/bin${PATH:+:${PATH}}"; export PATH;                                                                                                      
PERL5LIB="/home/ext/mr/smer/soniv/perl5/lib/perl5${PERL5LIB:+:${PERL5LIB}}"; export PERL5LIB;

# -------------------------------------------------------
#  Lien vers les executables
#~~~~~~ REBUILD
export EXE_REBUILD=/home/ext/mr/smer/brivoalt/NEMO4/trunk_r4.2-RC/tools/REBUILD_NEMO/rebuild_nemo
# CLASSIC PLOTS
basename=$1 
gridlist="1h_gridT 1h_gridV 1h_gridU 1h_gridV_15m 1h_gridU_15m 1h_gridT_15m 1d_gridW25h 1d_gridV_2D 1d_gridV25h 1d_gridU_2D 1d_gridU25h 1d_gridT25h 1d_gridS25h 1d_grid2D25h 1d_grid2D 1h_gridW"
NXIOS=100


# MOVE NOOBS DATA IN THEIR OWN DIRECTORY
mkdir NOOBS_DATA/
list1=$(ls ${basename}*NOOBS*_0000.nc)
for file1 in $list1
do
    mv ${file1%_0000.nc}_????.nc NOOBS_DATA/${grid}/
done


for grid in $gridlist ;
do   
   ./rebuild_pergrid.sh $basename $grid $NXIOS &
      echo $!
      pids="$pids $!"
done
for pid in $pids; do
    echo $pid
    wait $pid 

done


echo "REBUILD DONE"
if $CLEAN_AFTER_REBUILD;
then
    list2=$(ls ${basename}*_0000.nc)
    for file2 in $list2
    do
    if [ -f ${file2%_0000.nc}.nc ]; then
        ncdump -h ${file2%_0000.nc}.nc > ncdump_tmp.txt
        line_time=$( grep -n 'time_counter = UNLIMITED' ncdump_tmp.txt )
        tmp=$( echo $line_time | awk '{print $1}' )
        time_counter_len_tmp=$( echo $line_time | awk '{print $7}' )
        time_counter_len=$( echo -n $time_counter_len_tmp | tr -d '()' )
        if [ $((time_counter_len)) = 1 ] || [ $((time_counter_len)) = 24 ];
        then
 #          echo " ${file2%_0000.nc}.nc ok"
           rm -fv ${file2%_0000.nc}_????.nc
        else
           echo "file exists but ERROR with file ${file2%_0000.nc}.nc !!"
        fi
    else
           echo "ERROR with file ${file2%_0000.nc}.nc !!" 
    fi
    done
fi





