#!/bin/sh
basename=$1
grid=$2
NXIOS=$3

export EXE_REBUILD=/home/ext/mr/smer/brivoalt/NEMO4/trunk_r4.2-RC/tools/REBUILD_NEMO/rebuild_nemo

list_file_0000=$(ls ${basename}_${grid}_????????-????????_0000.nc)
for file_0000 in $list_file_0000
do
if [ -f ${file_0000%_0000.nc}.nc ]; then
   echo "file ${file_0000%_0000.nc}.nc exists, next"
   ncdump -h ${file_0000%_0000.nc}.nc > ncdump_tmp.txt
   line_time=$( grep -n 'time_counter = UNLIMITED' ncdump_tmp.txt )
   echo $line_time
   tmp=$( echo $line_time | awk '{print $1}' )
   time_counter_len_tmp=$( echo $line_time | awk '{print $7}' )
   time_counter_len=$( echo -n $time_counter_len_tmp | tr -d '()' )
   echo $time_counter_len
   if [ $((time_counter_len)) = 1 ] || [ $((time_counter_len)) = 24 ];
   then
      echo "next"
   else
      echo "But file ${file_0000%_0000.nc}.nc is broken !!!"
      srun --job-name=rebuild --partition=nmipt --ntasks=1 --cpus-per-task=8 --account=smer --time=01:00:00 time $EXE_REBUILD -p 8 ${file_0000%_0000.nc} $NXIOS
   fi
else
  srun --job-name=rebuild --partition=nmipt --ntasks=1 --cpus-per-task=8 --account=smer --time=01:00:00 time $EXE_REBUILD -p 8 ${file_0000%_0000.nc} $NXIOS
fi
done   





