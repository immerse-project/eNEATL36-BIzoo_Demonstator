# eNEATL36-AGRIF_Demonstator

This page describe the way to build a global 1/36° regional configuration other the North-East Atlantic (eNEATL36) with an embedded 1/108° AGRIF zoom.

## Status

The eNEATL36-AGRIF configuration is currently tested in NEMO4.2 over a smaller zoom in the bay of biscay. 

![Figure 1](https://github.com/immerse-project/eNEATL36-AGRIF_Demonstator/blob/main/FIGURES/figure_AGRIF.png)
_Figure : Snapshot of the surface current vorticity other the 1/36° eNEATL36 area (left) and other the 1/108° zoom area (right) after 1.5 month of simulation. The area contoured in dark is used to configure / test the model with AGRIF, whereas the target AGRIF zoom area is contoured in red._

## Intallation

* Download XIOS:

svn co -r 2130 http://forge.ipsl.jussieu.fr/ioserver/svn/XIOS/trunk XIOS

* Download NEMO trunk

svn co -r 14365 https://forge.ipsl.jussieu.fr/nemo/svn/NEMO/trunk trunk_r4.2-RC


## Compile

* On belenos : use the compilation script in https://github.com/immerse-project/eNEATL36-AGRIF_Demonstator/tree/main/SCRIPTS/COMPILE
* On other machines : use the compilation script, but update modules


## Run scripts

* example of run scripts here : https://github.com/immerse-project/eNEATL36-AGRIF_Demonstator/tree/main/SCRIPTS/RUN


