# eNEATL36-AGRIF_Demonstator

This page describe the way to build a global 1/36° regional configuration other the North-East Atlantic (eNEATL36) with an embedded 1/108° AGRIF zoom.

## Status

The eNEATL36-AGRIF configuration is currently has been tested in NEMO4.2 over a smaller zoom in the bay of biscay. The system is currently transferred on the target zoom area (contoured in red in Figure 1.)

![Figure 1](https://github.com/immerse-project/eNEATL36-AGRIF_Demonstator/blob/main/FIGURES/figure_AGRIF.png)
_Figure : Snapshot of the surface current vorticity other the 1/36° eNEATL36 area (left) and other the 1/108° AGRIF zoom (right) after 1.5 month of simulation. The area contoured in dark is used to configure / test the model with AGRIF, whereas the target AGRIF zoom area is contoured in red._

## Intallation

* Download XIOS:

`svn co -r 2130 http://forge.ipsl.jussieu.fr/ioserver/svn/XIOS/trunk XIOS`

* Download NEMO trunk

`svn co -r 14365 https://forge.ipsl.jussieu.fr/nemo/svn/NEMO/trunk trunk_r4.2-RC`


## How to compile

* How to compile

  1 : create the configuration : `./makenemo -m your_archfile -r eNEATL36_AGRIF -n AMM12 -j 20` 
  2 : Change cpp keys to : key_xios key_agrif key_vvl and add "NST" to your configuration in work_cfg.txt file
  3 : recompile : `./makenemo -m your_archfile -r eNEATL36_AGRIF -j 20`
  
* To clean the configuration : `./makenemo -m your_archfile -r eNEATL36_AGRIF -j 20 clean`

* An compilation script is also available in https://github.com/immerse-project/eNEATL36-AGRIF_Demonstator/tree/main/SCRIPTS/COMPILE . The list of modules necessary to compile on météo-france belenos supercomputer can be found in this script.

* Note that you also have compile the domain_cfg creation tool in order to perform a simulation. To do so, use `./maketools -n DOMAINcfg -m your_archfile` in the tools directory, with the cpp keys : key_mpp_mpi key_agrif.
## How to run

* example of run scripts here : https://github.com/immerse-project/eNEATL36-AGRIF_Demonstator/tree/main/SCRIPTS/RUN


