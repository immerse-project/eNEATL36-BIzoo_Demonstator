# eNEATL36-BIzoo (BIscay Zoom) Demonstator

This page describe the way to build a global 1/36° regional configuration other the North-East Atlantic (eNEATL36) with an embedded 1/108° AGRIF zoom.
It regroups:
- The eNEATL36 + BIZoo namelists and sources
- Some useful tools to create an AGRIF configuration from scratch, such as:
    - A tool to make the NEMO4.X coordinate file (domain_cfg.nc) compatible with the ifremer BMG tool (https://mars3d.ifremer.fr/Les-outils/BathyMeshGridTOOLS) in order to correct the bahtymetry manually (https://github.com/immerse-project/eNEATL36-BIzoo_Demonstator/tree/main/SCRIPTS/TOOLS/BATHY)
    - A tool to move the runoffs along a new coastline, and to extrapolate them on a higher resolution grid (in a nesting context) (https://github.com/immerse-project/eNEATL36-BIzoo_Demonstator/tree/main/SCRIPTS/TOOLS/MOVE_RUNOFFS)
- A wiki that details how to create an AGRIF configuration from scratch, and how to use the tools (https://github.com/immerse-project/eNEATL36-BIzoo_Demonstator/wiki) 

## Description

* Number of grid points : 9 321 751 (1294 * 1894 = 2 450 836 points for eNEATL36 plus 2559 * 2685 = 6 870 915 points for the AGRIF zoom)
* eNEATL36 : `lon_min = -19,91° ; lon_max = 22,67° ; lat_min = 26,10° ; lat_max = 64,15°`
* Zoom : `lon_min = -11,86° ; lon_max = 11,29° ; lat_min = 33,66° ; lat_max = 56,70°`
* Target period : Jan 2017 - June 2018

## Status

The eNEATL36-AGRIF configuration has been tested in NEMO4.2 over a smaller zoom in the bay of biscay. The system is currently transferred on the target zoom area (contoured in red in Figure 1.)

![Figure 1](https://github.com/immerse-project/eNEATL36-AGRIF_Demonstator/blob/main/FIGURES/figure_AGRIF.png)
_Figure : Snapshot of the surface current vorticity other the 1/36° eNEATL36 area (left) and other the 1/108° AGRIF zoom (right) after 1.5 month of simulation. The area contoured in dark is the high resolution nest area._

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

* A wiki is available and describe the procedure to recreate the eNEATL36 + BIZoo input mesh files : https://github.com/immerse-project/eNEATL36-BIzoo_Demonstator/wiki/ ; see sec. 1 and 2

## Run a eNEATL36-AGRIF simulation : 

* The wiki (sec 4.) describes how to run a simulation (https://github.com/immerse-project/eNEATL36-BIzoo_Demonstator/wiki)

## Additionnal tools : 

* A tool to update the runoffs files over the parent meshmask and to extrapolate it over the child grid is available here : https://github.com/immerse-project/eNEATL36-AGRIF_Demonstator/tree/main/SCRIPTS/TOOLS/MOVE_RUNOFFS
* Additional scripts to facilitate the use of the REBUILD_NEMO tool are available here : https://github.com/immerse-project/eNEATL36-AGRIF_Demonstator/tree/main/SCRIPTS/TOOLS/REBUILD
* The wiki also describe how to use the tools
