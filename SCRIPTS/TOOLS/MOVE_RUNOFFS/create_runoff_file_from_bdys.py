import shutil
from shutil import copyfile

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

# Namelist

year = 2019  # year of runoff file

# PATHS (Careful !!! Full path needed (e.g: /DATA/ROBERT/ instead of DATA/ROBERT))
rnf_bdy_folder = (
    "/data/vdi/tbrivoal/PRE_PROCESSING_IMMERSE/RUNOFFS_eNEATL36/rnf_forcing/"
)
CLIM_rnf_2D_file = (
    "/data/vdi/tbrivoal/PRE_PROCESSING_IMMERSE/RUNOFFS_eNEATL36/runoff_eNEATL36.nc"
)
coords_bdy_file = (
    "/data/vdi/tbrivoal/PRE_PROCESSING_IMMERSE/RUNOFFS_eNEATL36/coordinates.bdy.nc"
)
domain_cfg_file = (
    "/data/vdi/tbrivoal/PRE_PROCESSING_IMMERSE/RUNOFFS_eNEATL36/domain_cfg_init.nc"
)

output_folder = "/data/vdi/tbrivoal/PRE_PROCESSING_IMMERSE/RUNOFFS_eNEATL36/"
outfile = output_folder + "runoff_eNEATL36_BDY_only_y" + str(year) + ".nc"

test_script = False  # For debugging
rivers_only = True
clim_only = False
############# Read data ###############

file_rnf_bdy_U = xr.open_dataset(
    rnf_bdy_folder + "runoff_U_y" + str(year) + ".nc"
)  # file format : runoff_U_yYYYY.nc
file_rnf_bdy_V = xr.open_dataset(rnf_bdy_folder + "runoff_V_y" + str(year) + ".nc")
file_rnf_2D = xr.open_dataset(CLIM_rnf_2D_file)
file_coords_bdy = xr.open_dataset(coords_bdy_file)
domain_cfg = xr.open_dataset(
    domain_cfg_file,
    drop_variables={
        "x",
        "y",
    },
)

# Read river mouth coordinates
# ghosts cells are taken into account so we have to do - 2 (- 1 for ghost an -1 for python)

nbiu_gridT = file_rnf_bdy_U.nbidta.squeeze()  # - 1 # - 1 to convert to gridT
nbju_gridT = file_rnf_bdy_U.nbjdta.squeeze() - 1  # - 2
nbiv_gridT = file_rnf_bdy_V.nbidta.squeeze() - 1  # -2
nbjv_gridT = file_rnf_bdy_V.nbjdta.squeeze()  # - 1 # - 1 to convert to gridT

# Read BDY files of U & V runoffs

U_rnf_bdy = abs(file_rnf_bdy_U.runoffu.squeeze())
V_rnf_bdy = abs(file_rnf_bdy_V.runoffv.squeeze())

# Read 2D runoff data
rnf_2D = file_rnf_2D.orca_costal

# Read coordinates

mask = domain_cfg.top_level.squeeze()
e1t = domain_cfg.e1t.squeeze()
e2t = domain_cfg.e2t.squeeze()


################################## Convert montly clim to daily clim ###################################

# Date variables ----------------------------------------------------------------------------------------
dstart_year = str(year) + "-01-01"  # 1st day of the year
dend_year = str(year) + "-12-31"  # last day of the year

dstart_clim_monthly = str(year) + "-01-15"  # for 12 month clim
dend_clim_monthly = str(year) + "-12-15"  # for 12 month clim
dstart_minus_1_month = (
    str(year - 1) + "-12-01"
)  # used for conversion from monthly to daily clim data
# -----------------------------------

# Repare time dimension in the climatology -------------------------------------------------------------
time_counter_monthly = pd.date_range(
    dstart_clim_monthly, dend_clim_monthly, periods=12
)  # fake time dimension
rnf_2D["time_counter"] = time_counter_monthly

# Workaround : append last and first month of the climatology to the data ------------------------------
rnf_2D_minus_1 = rnf_2D[-1]
rnf_2D_minus_1 = rnf_2D_minus_1.expand_dims(
    "time_counter"
)  # workaround to keep a time dimension
rnf_2D_plus_1 = rnf_2D[0]
rnf_2D_plus_1 = rnf_2D_plus_1.expand_dims(
    "time_counter"
)  # workaround to keep a time dimension
rnf_2D_tmp = np.concatenate(
    (rnf_2D_minus_1.values, rnf_2D.values, rnf_2D_plus_1.values), axis=0
)

# Convert to rnf_2D_tmp (np.array) to xr.dataarray -----------------------------------------------------
time_counter_monthly_expand = pd.date_range(
    dstart_minus_1_month, freq="M", periods=14
)  # fake time dimension

rnf_2D_tmp_da = xr.DataArray(
    data=rnf_2D_tmp,
    dims=["time_counter", "y", "x"],
    coords=dict(time_counter=time_counter_monthly_expand),
)

# Resample data and repair time dimension --------------------------------------------------------------

rnf_2D_tmp_daily = rnf_2D_tmp_da.resample(time_counter="1D").interpolate("linear")
rnf_2D_daily = rnf_2D_tmp_daily[16:-16, :, :]  # select 365 days
time_counter_daily = pd.date_range(dstart_year, dend_year, freq="D")  # time dimension
rnf_2D_daily["time_counter"] = time_counter_daily  # repare time dimension
del (rnf_2D_tmp_daily, rnf_2D_tmp, rnf_2D_minus_1, rnf_2D_plus_1)


############################ Append 3D bdy runoffs to the climatology ###################################

Rho = 1000.0

# now add runoff BDY data over the climatology data
if test_script == True:
    rnf_2D_daily_new = rnf_2D_daily  # initialisation
    rnf_2D_daily_new[:, :, :] = 0.0  # initialisation
else:
    rnf_2D_daily_new = rnf_2D_daily  # initialisation

if rivers_only == True:
    rnf_2D_daily_new = rnf_2D_daily  # initialisation
    rnf_2D_daily_new[:, :, :] = 0.0  # initialisation
else:
    rnf_2D_daily_new = rnf_2D_daily  # initialisation

if clim_only == False:
    for ind in range(len(U_rnf_bdy[0, :])):
        #     print(ind, nbju_gridT[ind].values,nbiu_gridT[ind].values)
        e1te2t = (
            e1t[nbju_gridT[ind], nbiu_gridT[ind]]
            * e2t[nbju_gridT[ind], nbiu_gridT[ind]]
        )
        rnf_2D_daily_new[:, nbju_gridT[ind], nbiu_gridT[ind]] = rnf_2D_daily_new[
            :, nbju_gridT[ind], nbiu_gridT[ind]
        ] + ((U_rnf_bdy[:, ind].values * Rho) / e1te2t.values)

    for ind in range(len(V_rnf_bdy[0, :])):
        e1te2t = (
            e1t[nbjv_gridT[ind], nbiv_gridT[ind]]
            * e2t[nbjv_gridT[ind], nbiv_gridT[ind]]
        )
        rnf_2D_daily_new[:, nbjv_gridT[ind], nbiv_gridT[ind]] = rnf_2D_daily_new[
            :, nbjv_gridT[ind], nbiv_gridT[ind]
        ] + ((V_rnf_bdy[:, ind].values * Rho) / e1te2t.values)

#
if test_script == True:
    TEST = rnf_2D_daily_new.where(mask.values == 0, 0.0)  # mask sea data for testing
    if np.nanmean(TEST.values) == 0:
        print("TEST OK")
    else:
        print("TEST NOK", str(np.nanmean(TEST.values)))


############################ Save in a Netcdf ###################################
time_counter_daily = pd.date_range(dstart_year, dend_year, freq="D")  # time dimension

# time_counter_daily_float = pd.to_numeric(time_counter_daily, downcast='float')
# time_counter_daily.values.astype("float")
# Create xarray dataarray
rnf_2D_daily_new_da = xr.DataArray(
    data=rnf_2D_daily_new,
    dims=["time_counter", "y", "x"],
    coords=dict(time_counter=time_counter_daily.values),
    attrs=rnf_2D.attrs,
    name=rnf_2D.name,
)

# Create dataset
ds = xr.merge([rnf_2D_daily_new_da, file_rnf_2D.nav_lat, file_rnf_2D.nav_lon])
ds.attrs = file_rnf_2D.attrs
# Save to netcdf
ds.to_netcdf(outfile, mode="w")
