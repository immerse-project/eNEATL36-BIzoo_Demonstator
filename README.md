# eNEATL36-AGRIF_Demonstator

This page describe the way to build a global 1/36° regional configuration other the North-East Atlantic (eNEATL36) with an embedded 1/108° AGRIF zoom.

## Description

* Number of grid points : 9 321 751 (1294 * 1894 = 2 450 836 points for eNEATL36 plus 2559 * 2685 = 6 870 915 points for the AGRIF zoom)
* eNEATL36 : `lon_min = -19,91° ; lon_max = 22,67° ; lat_min = 26,10° ; lat_max = 64,15°`
* Zoom : `lon_min = -11,86° ; lon_max = 11,29° ; lat_min = 33,66° ; lat_max = 56,70°`
* Target period : Jan 2017 - June 2018

## Status

The eNEATL36-AGRIF configuration has been tested in NEMO4.2 over a smaller zoom in the bay of biscay. The system is currently transferred on the target zoom area (contoured in red in Figure 1.)

![Figure 1](https://github.com/immerse-project/eNEATL36-AGRIF_Demonstator/blob/main/FIGURES/figure_AGRIF.png)
_Figure : Snapshot of the surface current vorticity other the 1/36° eNEATL36 area (left) and other the 1/108° AGRIF zoom (right) after 1.5 month of simulation. The area contoured in dark is the high resolution nest area.

## Intallation

* Download XIOS:

`svn co -r 2130 http://forge.ipsl.jussieu.fr/ioserver/svn/XIOS/trunk XIOS`

* Download NEMO trunk

`git clone --branch 4.2.0 https://forge.nemo-ocean.eu/nemo/nemo.git nemo_4.2.0`


## How to compile

 
  1 : create the configuration : `./makenemo -m your_archfile -r eNEATL36_AGRIF -n AMM12 -j 20`   
  2 : Change cpp keys to : key_xios key_agrif key_qco and add "NST" to your configuration in work_cfg.txt file   
  3 : clean and recompile : 
  `./makenemo -m your_archfile -r eNEATL36_AGRIF -j 20 clean`
  `./makenemo -m your_archfile -r eNEATL36_AGRIF -j 20`   
  
* An compilation script is also available in https://github.com/immerse-project/eNEATL36-AGRIF_Demonstator/tree/main/SCRIPTS/COMPILE . The list of modules necessary to compile on météo-france belenos supercomputer can be found in this script.

* Note that you also have compile the domain_cfg creation tool in order to perform a simulation. To do so, use `./maketools -n DOMAINcfg -m your_archfile` in the tools directory, with the cpp keys : key_mpp_mpi key_agrif.

## Create the input mesh files : 

* Launch domaincfg tool with the namelists in :
https://github.com/immerse-project/eNEATL36-AGRIF_Demonstator/tree/main/NAMELISTS/DOMAINCFG
* An example of domain_cfg slurm script is available here : 
https://github.com/immerse-project/eNEATL36-AGRIF_Demonstator/blob/main/SCRIPTS/DOMAINcfg/run_domain_cfg_eNEATL36_AGRIF_emodNET2018_finaldomain_corrected_with_FES2014.sub

## Run a eNEATL46-AGRIF simulation : 

* Use the run scripts here : 
https://github.com/immerse-project/eNEATL36-AGRIF_Demonstator/tree/main/SCRIPTS/RUN :   

1 : Copy the 3 scripts (NEMO_4_2_AGRIF_RUN_INI.sub, NEMO_4_2_AGRIF_RUN_RESTART.sub and NEMO_4_2_AGRIF_RUN.sub.model) in the run directory   
2 : Change paths (and modules eventually) in `NEMO_4_2_AGRIF_RUN_INI.sub`   
3 : submit INI job `sbatch NEMO_4_2_AGRIF_RUN_INI.sub`  

* The namelists for the simulation are available here : 
https://github.com/immerse-project/eNEATL36-AGRIF_Demonstator/tree/main/NAMELISTS/RUN 

* The namelists for XIOS are available here : 
https://github.com/immerse-project/eNEATL36-AGRIF_Demonstator/tree/main/NAMELISTS/XML


## Additionnal tools : 

* A tool to update the runoffs files over the parent meshmask and to extrapolate it over the child grid is available here : https://github.com/immerse-project/eNEATL36-AGRIF_Demonstator/tree/main/SCRIPTS/TOOLS/MOVE_RUNOFFS
* Additional scripts to facilitate the use of the REBUILD_NEMO tool are available here : https://github.com/immerse-project/eNEATL36-AGRIF_Demonstator/tree/main/SCRIPTS/TOOLS/REBUILD
