#!/usr/bin/env python3

import decimal
import shutil
import sys
import time
from shutil import copyfile

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr


######################################################################################################################
def check_mask_nearby_ij(i, j, mask, ndist):
    # Function to count how many land points are found along i (TEST_i) and j (TEST_j) direction
    # i,j = indexes of the point to test
    # mask = 2D mask
    # ndist = distance from center to check
    if i > (ndist - 1):
        TEST_i = np.nansum(mask[i - ndist : i + ndist + 1, j])
    else:
        TEST_i = np.nansum(mask[i : i + ndist + 1, j])
    if j > (ndist - 1):
        TEST_j = np.nansum(mask[i, j - ndist : j + ndist + 1])
    else:
        TEST_j = np.nansum(mask[i, j : j + ndist + 1])
    return TEST_i, TEST_j


######################################################################################################################
def check_if_surrounded_by_land(i, j, mask, ndist):
    # Function to check if the point at i,j is surrounded by land
    # It counts how many land points (npts) are around in a ndist perimeter
    # 	CASE 1 : if npts = sum of the number of all points in the ndist perimeter = the point is surrounded by land
    # 	Then = return surrounded_by_land=1
    #   CASE 2 : if npts != sum of the number of all points in the ndist perimeter = at least one sea point is found in ndist perimeter
    #   Then = return surrounded_by_land=0

    surrounded_by_land = 0
    dim_i, dim_j = int(len(mask[:, 0])), int(len(mask[0, :]))
    # i = index along i of point to test
    # j = index along j of point to test
    # mask = 2D mask
    # ndist = distance from center to check

    # print(i, ' CASE1 ', (ndist-1), ' CASE2 ' ,((dim_i-1) - ndist))
    if i >= (ndist - 1):
        if j >= (ndist - 1):
            npts = np.nansum(mask[i - ndist : i + ndist + 1, j - ndist : j + ndist + 1])
            if npts == (1 + (ndist * 2)) ** 2:
                surrounded_by_land = 1
        else:
            npts = np.nansum(mask[i - ndist : i + ndist + 1, j : j + ndist + 1])
            if npts == (1 + (ndist * 2)) * (1 + (ndist * 2) - ndist):
                surrounded_by_land = 1
    else:
        if j >= (ndist - 1):
            npts = np.nansum(mask[i : i + ndist + 1, j - ndist : j + ndist + 1])
            if npts == (1 + (ndist * 2)) * (1 + (ndist * 2) - ndist):
                surrounded_by_land = 1
        else:
            npts = np.nansum(mask[i : i + ndist + 1, j : j + ndist + 1])
            if npts == (1 + (ndist * 2) - ndist) * (1 + (ndist * 2) - ndist):
                surrounded_by_land = 1

    if i <= ((dim_i - 1) - ndist):
        if j <= ((dim_j - 1) - ndist):
            npts = np.nansum(mask[i - ndist : i + ndist + 1, j - ndist : j + ndist + 1])
            if npts == (1 + (ndist * 2)) ** 2:
                surrounded_by_land = 1
        else:
            npts = np.nansum(mask[i - ndist : i + ndist + 1, j - ndist : j + 1])
            if npts == (1 + (ndist * 2)) * (1 + (ndist * 2) - ndist):
                surrounded_by_land = 1
    else:
        if j <= ((dim_j - 1) - ndist):
            npts = np.nansum(mask[i - ndist : i + ndist + 1, j - ndist : j + ndist + 1])
            if npts == (1 + (ndist * 2)) * (1 + (ndist * 2) - ndist):
                surrounded_by_land = 1
        else:
            npts = np.nansum(mask[i - ndist : i + 1, j - ndist : j + ndist])
            if npts == (1 + (ndist * 2) - ndist) * (1 + (ndist * 2) - ndist):
                surrounded_by_land = 1
    return surrounded_by_land


######################################################################################################################
def check_if_surrounded_by_sea(i, j, mask, ndist, nseuil):
    # Same as check_if_surrounded_by_land, but the mask is inverted.
    # Thus, it returns surrounded_by_sea=1 if the point is surrounded by sea, or 0 if at least one land point is found in the perimeter
    mask_inv = np.where(mask == 1, 0, 1)
    surrounded_by_sea = 0
    dim_i, dim_j = int(len(mask_inv[:, 0])), int(len(mask_inv[0, :]))
    # i = index along i of point to test
    # j = index along j of point to test
    # mask_inv = 2D mask_inv
    # ndist = distance from center to check
    if i >= (ndist - 1):
        if j >= (ndist - 1):
            npts = np.nansum(
                mask_inv[i - ndist : i + ndist + 1, j - ndist : j + ndist + 1]
            )
            if npts == (1 + (ndist * 2)) ** 2:
                surrounded_by_sea = 1

        else:
            npts = np.nansum(mask_inv[i - ndist : i + ndist + 1, j : j + ndist + 1])
            if npts == (1 + (ndist * 2)) * (1 + (ndist * 2) - ndist):
                surrounded_by_sea = 1

    else:
        if j >= (ndist - 1):
            npts = np.nansum(mask_inv[i : i + ndist + 1, j - ndist : j + ndist + 1])
            if npts == (1 + (ndist * 2)) * (1 + (ndist * 2) - ndist):
                surrounded_by_sea = 1

        else:
            npts = np.nansum(mask_inv[i : i + ndist + 1, j : j + ndist + 1])
            if npts == (1 + (ndist * 2) - ndist) * (1 + (ndist * 2) - ndist):
                surrounded_by_sea = 1
    if i <= ((dim_i - 1) - ndist):
        if j <= ((dim_j - 1) - ndist):
            npts = np.nansum(
                mask_inv[i - ndist : i + ndist + 1, j - ndist : j + ndist + 1]
            )
            if npts == (1 + (ndist * 2)) ** 2:
                surrounded_by_sea = 1

        else:
            npts = np.nansum(mask_inv[i - ndist : i + ndist + 1, j - ndist : j + ndist])
            if npts == (1 + (ndist * 2)) * (1 + (ndist * 2) - ndist):
                surrounded_by_sea = 1

    else:
        if j <= ((dim_j - 1) - ndist):
            npts = np.nansum(mask_inv[i - ndist : i + ndist, j - ndist : j + ndist + 1])
            if npts == (1 + (ndist * 2)) * (1 + (ndist * 2) - ndist):
                surrounded_by_sea = 1

        else:
            npts = np.nansum(mask_inv[i - ndist : i + ndist, j - ndist : j + ndist])
            if npts == (1 + (ndist * 2) - ndist) * (1 + (ndist * 2) - ndist):
                surrounded_by_sea = 1

    return surrounded_by_sea


######################################################################################################################
def find_nearest_sea_point(i, j, mask, ndist):
    # Function to find the nearest sea point of point at i,j
    # This function is called when a runoff point is found on a land point, and when there is at least one sea point in ndist perimeter
    # It returns preferentially the indexes of (in the following order):
    # - CASE 1: the sea points in ndist perimeter along i and j direction
    # - CASE 2: is CASE 1 does not exists, the sea points in ndist perimeter along the diagonals
    # First, select the mask around a ndist perimeter of the point at (i,j)

    if i > (ndist - 1):
        if j > (ndist - 1):
            arr_m = mask[i - ndist : i + ndist + 1, j - ndist : j + ndist + 1]
        else:
            arr_m = mask[i - ndist : i + ndist + 1, j : j + ndist + 1]
    else:
        if j > (ndist - 1):
            arr_m = mask[i : i + ndist + 1, j - ndist : j + ndist + 1]
        else:
            arr_m = mask[i : i + ndist + 1, j : j + ndist + 1]

    arr_m_ij = np.ones(arr_m.shape)
    arr_m_ij[ndist, :] = arr_m[ndist, :]
    arr_m_ij[:, ndist] = arr_m[:, ndist]

    # First check => if there is a sea point along i, j directions only
    if 0 in arr_m_ij:  # CASE 1
        available_points = np.argwhere(arr_m_ij[:, :] == 0) - ndist
        available_points[:, 0] = available_points[:, 0] + i
        available_points[:, 1] = available_points[:, 1] + j
    # Second check => if there is a sea point along all directions
    elif 0 in arr_m:  # CASE 2
        available_points = np.argwhere(arr_m[:, :] == 0) - ndist
        available_points[:, 0] = available_points[:, 0] + i
        available_points[:, 1] = available_points[:, 1] + j
    else:
        print("ERROR")
        print(arr_m)
    return available_points


######################################################################################################################
def get_nearest_coast_point(i, j, ndist, nearests_land_points):
    # Function to return the nearest coast point of a runoff point at i,j, from a list of nearest sea points nearests_land_points found precendently
    # => For a land point at iland, jland :
    # the index along x direction (icoast) of the nearest coast point is :
    # - iland -1 if iland > i
    # - iland if iland=i
    # - iland + 1 if iland < i
    # The same find is done for y axes.

    nearests_coast_point = np.zeros(nearests_land_points.shape)
    if i < (ndist - 1):
        if j < (ndist - 1):
            nearests_coast_point[:, 0] = (
                nearests_land_points[:, 0] + i - (ndist - 1)
            )  # Go back to real indexes
            nearests_coast_point[:, 1] = (
                nearests_land_points[:, 1] + j - (ndist - 1)
            )  # Go back to real indexes
            nearests_coast_point[:, 0] = np.where(
                nearests_coast_point[:, 0] > i,
                nearests_coast_point[:, 0] - 1,
                nearests_coast_point[:, 0],
            )
            nearests_coast_point[:, 1] = np.where(
                nearests_coast_point[:, 1] > j,
                nearests_coast_point[:, 1] - 1,
                nearests_coast_point[:, 1],
            )
        else:
            nearests_coast_point[:, 0] = (
                nearests_land_points[:, 0] + i - (ndist - 1)
            )  # Go back to real indexes
            nearests_coast_point[:, 1] = (
                nearests_land_points[:, 1] + j - ndist
            )  # Go back to real indexes
            nearests_coast_point[:, 0] = np.where(
                nearests_coast_point[:, 0] < i,
                nearests_coast_point[:, 0] + 1,
                nearests_coast_point[:, 0],
            )
            nearests_coast_point[:, 0] = np.where(
                nearests_coast_point[:, 0] > i,
                nearests_coast_point[:, 0] - 1,
                nearests_coast_point[:, 0],
            )
            nearests_coast_point[:, 1] = np.where(
                nearests_coast_point[:, 1] < j,
                nearests_coast_point[:, 1] + 1,
                nearests_coast_point[:, 1],
            )
            nearests_coast_point[:, 1] = np.where(
                nearests_coast_point[:, 1] > j,
                nearests_coast_point[:, 1] - 1,
                nearests_coast_point[:, 1],
            )
    else:
        nearests_coast_point[:, 0] = (
            nearests_land_points[:, 0] + i - ndist
        )  # Go back to real indexes
        nearests_coast_point[:, 1] = (
            nearests_land_points[:, 1] + j - ndist
        )  # Go back to real indexes
        nearests_coast_point[:, 0] = np.where(
            nearests_coast_point[:, 0] < i,
            nearests_coast_point[:, 0] + 1,
            nearests_coast_point[:, 0],
        )
        nearests_coast_point[:, 0] = np.where(
            nearests_coast_point[:, 0] > i,
            nearests_coast_point[:, 0] - 1,
            nearests_coast_point[:, 0],
        )
        nearests_coast_point[:, 1] = np.where(
            nearests_coast_point[:, 1] < j,
            nearests_coast_point[:, 1] + 1,
            nearests_coast_point[:, 1],
        )
        nearests_coast_point[:, 1] = np.where(
            nearests_coast_point[:, 1] > j,
            nearests_coast_point[:, 1] - 1,
            nearests_coast_point[:, 1],
        )

    return nearests_coast_point


######################################################################################################################
def find_nearest_coast_point(i, j, mask, ndist):
    # This function does basically the same operations as find_nearest_sea_point, except that:
    #    - the mask is inverted - so that the function looks for the closest land point
    #    - it does not returns directly the closest land point, but the nearest point in the sea by calling the function get_nearest_coast_point
    # The closest land point(s) found will be preferentially:
    # - CASE 1: the land point(s) in ndist perimeter along i and j direction
    # - CASE 2: is CASE 1 does not exists, the land point(s) in ndist perimeter along the diagonals

    mask_inv = np.where(mask == 1, 0, 1)  # invert mask
    idim, jdim = int(len(mask[:, 0])), int(len(mask[0, :]))

    if i > (ndist - 1):
        if j > (ndist - 1):
            arr_m = mask_inv[i - ndist : i + ndist + 1, j - ndist : j + ndist + 1]
        else:
            arr_m = mask_inv[i - ndist : i + ndist + 1, j : j + ndist + 1]
    else:
        if j > (ndist - 1):
            arr_m = mask_inv[i : i + ndist + 1, j - ndist : j + ndist + 1]
        else:
            arr_m = mask_inv[i : i + ndist + 1, j : j + ndist + 1]

    arr_m_ij = np.ones(arr_m.shape)
    arr_m_ij[ndist, :] = arr_m[ndist, :]
    arr_m_ij[:, ndist] = arr_m[:, ndist]
    if 0 in arr_m_ij:  # CASE 1
        # check along i and j axis only
        nearests_land_points = np.argwhere(arr_m_ij[:, :] == 0)
        available_points = get_nearest_coast_point(i, j, ndist, nearests_land_points)
    elif 0 in arr_m:  # CASE 2
        nearests_land_points = np.argwhere(arr_m[:, :] == 0)
        available_points = get_nearest_coast_point(i, j, ndist, nearests_land_points)
    else:
        print("ERROR")
        print(arr)
    return available_points


######################################################################################################################
def move_runoffs(rnf_2Dt, rnf_point, mask, verb):
    # --------------------------------------------------------------------------------------------------
    # PURPOSE :
    # Check runoff data and move data off the coast or over land at the first available point near the coast
    # ------------------------------------
    # CASE 1 : Runoff point is over land :
    # find the nearest(s) sea point(s) and return its (their) index : ind=(i,j) or ind(i1,j1,i2,j2....)
    # 2 possibilities :
    #    => At least one runoff value at ind=(in,jn) is 0.0 : move data over this point
    #    => No runoff value at ind=(in,jn) is > 0.0 : add runoff value to this point
    # When more than one sea point is found (ind(i1,j1,i2,j2....)), the runoff is averaged over every points
    #
    # ------------------------------------
    # CASE 2 : Runoff point is surrounded by sea :
    # Find the nearest coast point
    # If more than one coast points are available, average avor the two coast points
    #
    #
    # --------------------------------------------------------------------------------------------------
    # Inputs :
    # rnf_2D = runoff data in 2 dimension
    # rnf_point = array with indexes of rnf points (should have the form : (2,N),
    # where N is the number of runoff points)
    # mask = output mask (1 over sea points and 0 over land points)
    # verb = verbose (True or False)
    # --------------------------------------------------------------------------------------------------
    # Output : New 2D array with moved runoffs
    # --------------------------------------------------------------------------------------------------

    # Initialisation
    nseuil = 30  # over 30 points distance, do not replace runoff
    rnf_2D = rnf_2Dt[0, :, :]
    rnf_2Dt_new = np.copy(rnf_2Dt)
    # rnf_2Dt_new[:,:,:] = 0.
    mask_data = mask
    mask_data = np.where(mask_data == 1, 0, 1)  # invert mask
    sea_point_not_found = 0.0
    land_point_not_found = 0.0
    ndist = 1

    # --------------------------------------------------------------------------------------------------
    # BEGIN LOOP
    print(len(rnf_point[0, :]))
    # Loop over valid runoff values only
    for n in range(len(rnf_point[0, :])):
        if verb:
            print(
                "treating runoff point ",
                rnf_point[0, n],
                rnf_point[1, n],
                n,
                "/",
                len(rnf_point[0, :]),
            )

        if mask_data[rnf_point[0, n], rnf_point[1, n]] == 1:  # CASE 1 -> Rnf over land
            surrounded = check_if_surrounded_by_land(
                rnf_point[0, n], rnf_point[1, n], mask_data, ndist
            )
            if verb:
                print(
                    "==> j, i = ", rnf_point[0, n], rnf_point[1, n], "is on mask point"
                )

            if surrounded == 1:  # Surrounded by earth
                # Here, we will extend ndist and check again if the point is surrounded by land until ndist > nseuil
                # If ndist > nseuil => We print a warning, but we do nothing
                if ndist > nseuil:
                    print(
                        "WARNING !!! : closest sea point is over ",
                        nseuil,
                        "point perimeter at i, j = ",
                        rnf_point[0, n],
                        rnf_point[1, n],
                    )
                else:
                    while sea_point_not_found == 0:
                        surrounded = check_if_surrounded_by_land(
                            rnf_point[0, n], rnf_point[1, n], mask_data, ndist
                        )

                        if surrounded == 1:  # No sea point in ndist perimeter
                            if verb:
                                print(
                                    rnf_point[0, n],
                                    rnf_point[1, n],
                                    "surrounded by earth points, trying ndist=+1;",
                                    "next radius = ",
                                    (1 + ((ndist + 1) * 2)),
                                )
                        else:  # At least one sea point in ndist perimeter
                            sea_point_not_found = 1.0
                            indexes_closests_sea_point = find_nearest_sea_point(
                                rnf_point[0, n], rnf_point[1, n], mask_data, ndist
                            )
                        ndist = ndist + 1

            else:  # AT LEAST ONE SEA POINT in ndist=1 perimeter ------------
                indexes_closests_sea_point = find_nearest_sea_point(
                    rnf_point[0, n], rnf_point[1, n], mask_data, ndist
                )
            # NOW REPLACE RUNOFFS
            npoints = len(indexes_closests_sea_point[:, 0])
            # Now replace data
            if npoints == 0:
                # No available points nearby without an already existing runoff value => avoid
                # rnf_2Dt_new[:,rnf_point[0,n],rnf_point[1,n]] = 0.
                print(rnf_point[0, n], rnf_point[1, n], "ISSUE AT THIS POINT !!")
            else:
                tmp = 0
                for ind in range(npoints):
                    if verb:
                        print(
                            "moving point over ",
                            npoints,
                            "points : i,j ",
                            ind + 1,
                            "/",
                            npoints,
                            ":",
                            "=",
                            int(indexes_closests_sea_point[ind, 0]),
                            int(indexes_closests_sea_point[ind, 1]),
                        )
                    rnf_2Dt_new[
                        :,
                        int(indexes_closests_sea_point[ind, 0]),
                        int(indexes_closests_sea_point[ind, 1]),
                    ] = rnf_2Dt_new[
                        :,
                        int(indexes_closests_sea_point[ind, 0]),
                        int(indexes_closests_sea_point[ind, 1]),
                    ] + rnf_2Dt_new[
                        :, rnf_point[0, n], rnf_point[1, n]
                    ] / float(
                        npoints
                    )

                rnf_2Dt_new[:, rnf_point[0, n], rnf_point[1, n]] = 0.0

        else:  # CASE 2: POINT IS OVER SEA ------------
            ndist = 1
            surrounded = check_if_surrounded_by_sea(
                rnf_point[0, n], rnf_point[1, n], mask_data, ndist, 3
            )
            # Loop until we find at least one sea point in ndist perimeter$
            if surrounded == 1:  # Surrounded by sea
                if verb:
                    print(
                        "==> j, i = ",
                        rnf_point[0, n],
                        rnf_point[1, n],
                        "is surrounded by sea ",
                    )
                if ndist > nseuil:
                    print(
                        "WARNING !!! : closest land point is over ",
                        nseuil,
                        "point perimeter at i, j = ",
                        rnf_point[0, n],
                        rnf_point[1, n],
                    )
                else:
                    while land_point_not_found == 0:
                        surrounded = check_if_surrounded_by_sea(
                            rnf_point[0, n], rnf_point[1, n], mask_data, ndist, 3
                        )

                        if surrounded == 1:  # No sea point in ndist perimeter
                            if verb:
                                print(
                                    rnf_point[0, n],
                                    rnf_point[1, n],
                                    "surrounded by sea points, trying ndist=+1;",
                                    "next radius = ",
                                    (1 + ((ndist + 1) * 2)),
                                )
                        else:  # At least one sea point in ndist perimeter
                            land_point_not_found = 1.0
                            indexes_closests_land_point = find_nearest_coast_point(
                                rnf_point[0, n], rnf_point[1, n], mask_data, ndist
                            )

                        ndist = ndist + 1
                    # NOW REPLACE RUNOFFS
                    npoints = len(indexes_closests_land_point[:, 0])
                    # Now replace data
                    if npoints == 0:
                        # No available points nearby without an already existing runoff value => avoid
                        # rnf_2Dt_new[:,rnf_point[0,n],rnf_point[1,n]] = 0.
                        print(
                            rnf_point[0, n], rnf_point[1, n], "ISSUE AT THIS POINT !!"
                        )
                    else:
                        for ind in range(npoints):
                            if verb:
                                print(
                                    "moving point over ",
                                    npoints,
                                    "points, : i, j =",
                                    int(indexes_closests_land_point[ind, 0]),
                                    int(indexes_closests_land_point[ind, 1]),
                                )
                            rnf_2Dt_new[
                                :,
                                int(indexes_closests_land_point[ind, 0]),
                                int(indexes_closests_land_point[ind, 1]),
                            ] = rnf_2Dt_new[
                                :,
                                int(indexes_closests_land_point[ind, 0]),
                                int(indexes_closests_land_point[ind, 1]),
                            ] + rnf_2Dt_new[
                                :, rnf_point[0, n], rnf_point[1, n]
                            ] / float(
                                npoints
                            )

                        rnf_2Dt_new[:, rnf_point[0, n], rnf_point[1, n]] = 0
        sea_point_not_found = 0.0
        land_point_not_found = 0.0
        ndist = 1
    if verb:
        print("..........")

    # Next point
    return rnf_2Dt_new


# --------------------------------------------------------------------------------------------------
# END LOOP


######################################################################################################################
def find_nearest_coast_point_ij(i, j, mask, rnf_data, nseuil):
    # This function is used in move_runoffs_ij
    # It finds the nearest coast point along ij direction only
    out = []
    n = 1
    var = 0
    nip1, nim1, njp1, njm1 = 0, 0, 0, 0
    while (var == 0) and (n < nseuil):
        if mask[i + n, j] == 1:
            if (
                rnf_data[0, i + n - 1, j] == 0.0
            ):  # Nb: All conditions here assumes runoffs does not move through time
                if mask[i + n - 1, j] == 0.0:
                    out = np.append(out, [i + n - 1, j])
                else:
                    nip1 = 1
        if mask[i - n, j] == 1:
            if rnf_data[0, i - n + 1, j] == 0.0:
                if mask[i - n + 1, j] == 0.0:
                    out = np.append(out, [i - n + 1, j])
                else:
                    nim1 = 1
        if mask[i, j + n] == 1:
            if rnf_data[0, i, j + n - 1] == 0.0:
                if mask[i, j + n - 1] == 0.0:
                    out = np.append(out, [i, j + n - 1])
                else:
                    njp1 = 1
        if mask[i, j - n] == 1:
            if rnf_data[0, i, j - n + 1] == 0.0:
                if mask[i, j - n + 1] == 0.0:
                    out = np.append(out, [i, j - n + 1])
                else:
                    njm1 = 1

        var = len(out)
        if var == 0:  # In case we have gone too far
            if nip1 == 1:
                out = np.append(out, [i + n - 2, j])
            if nim1 == 1:
                out = np.append(out, [i - n + 2, j])
            if njp1 == 1:
                out = np.append(out, [i, j + n - 2])
            if njm1 == 1:
                out = np.append(out, [i, j - n + 2])
        n = n + 1
        var = len(out)

    return out  # closest coastal point


######################################################################################################################
def move_runoffs_ij(rnf_2D, rnf_point, mask, verb):
    # --------------------------------------------------------------------------------------------------
    # PURPOSE :
    # Check runoff data and move data off the coast or over land at the first available along i,j
    # ------------------------------------
    # CASE 1 : at least one earth point in i, j
    # ------------------------------------
    # CASE 2 : Runoff point is surrounded by sea :
    # Find the nearest coast point
    # If more than one coast points are available, average avor the two coast points
    #
    #
    # --------------------------------------------------------------------------------------------------
    # Inputs :
    # rnf_2D = runoff data in 2 dimension
    # rnf_point = array with indexes of rnf points (should have the form : (2,N),
    # where N is the number of runoff points)
    # mask = output mask (1 over sea points and 0 over land points)
    # verb = verbose (True or False)
    # --------------------------------------------------------------------------------------------------
    # Output : New 2D array with moved runoffs
    # --------------------------------------------------------------------------------------------------

    # Initialisation
    nseuil = 4  # over 4 points distance, do not replace runoff
    rnf_2D_new = np.copy(rnf_2D)
    mask_data = mask
    mask_data = np.where(mask_data == 1, 0, 1)  # invert mask
    sea_point_not_found = 0.0
    ndist = 1

    # --------------------------------------------------------------------------------------------------
    # BEGIN LOOP

    # Loop over valid runoff values only
    for n in range(len(rnf_point[0, :])):
        N_earth_points_i, N_earth_points_j = check_mask_nearby_ij(
            rnf_point[0, n], rnf_point[1, n], mask_data, ndist
        )
        N_earth_points_ij = N_earth_points_i + N_earth_points_j
        if N_earth_points_ij > 0:  # at least one earth point nearby
            if verb:
                print("==> j, i = ", rnf_point[0, n], rnf_point[1, n], "ok")

        # POINT IS SURROUNDED BY SEA along i and j------------
        else:  # no earth point nearby

            if verb:
                print(
                    rnf_point[0, n],
                    rnf_point[1, n],
                    "is in the middle of the sea",
                    N_earth_points_i,
                    N_earth_points_j,
                    mask_data[rnf_point[0, n] + 1, rnf_point[1, n]],
                )
            # ------------------------------------------------
            # Find nearest coast point from 1 to nseuil distance
            ind = find_nearest_coast_point_ij(
                rnf_point[0, n], rnf_point[1, n], mask_data, rnf_2D, nseuil
            )
            npoints = len(ind) / 2
            # ------------------------------------------------

            if (
                npoints == 0
            ):  # No available points nearby without an already existing runoff value => avoid
                # rnf_2D_new[rnf_point[0,n],rnf_point[1,n]] = 0.
                print(
                    "WARNING : could not find a coast point at a distance < ",
                    nseuil,
                    " for point at i, j = ",
                    rnf_point[0, n],
                    rnf_point[1, n],
                    ", This point might be in a corner (or if not, there is a bug)",
                )
            if npoints == 1:
                rnf_2D_new[:, int(ind[0]), int(ind[1])] = (
                    rnf_2D_new[:, int(ind[0]), int(ind[1])]
                    + rnf_2D_new[:, rnf_point[0, n], rnf_point[1, n]]
                )
                rnf_2D_new[:, rnf_point[0, n], rnf_point[1, n]] = 0.0
                if verb:
                    print(
                        "moving point j,i = ",
                        rnf_point[0, n],
                        rnf_point[1, n],
                        "at point j,i = ",
                        ind,
                    )
            if npoints == 2:
                rnf_2D_new[:, int(ind[0]), int(ind[1])] = rnf_2D_new[
                    :, int(ind[0]), int(ind[1])
                ] + (rnf_2D_new[:, rnf_point[0, n], rnf_point[1, n]] / 2)
                rnf_2D_new[:, int(ind[2]), int(ind[3])] = rnf_2D_new[
                    :, int(ind[2]), int(ind[3])
                ] + (rnf_2D_new[:, rnf_point[0, n], rnf_point[1, n]] / 2)
                rnf_2D_new[:, rnf_point[0, n], rnf_point[1, n]] = 0.0
                if verb:
                    print(
                        "dispatch point j,i = ",
                        rnf_point[0, n],
                        rnf_point[1, n],
                        "at 2 points j1,i1,j2,i2 = ",
                        ind,
                    )
            if npoints > 2:
                print("OVER 2")
            if verb:
                print("..........")

        sea_point_not_found = 0.0
        ndist = 1
        # Next point
    return rnf_2D_new


# --------------------------------------------------------------------------------------------------
# END LOOP


######################################################################################################################
# MAIN PROGRAM #
######################################################################################################################

year = 2018

rnf_inp_file = "RNF_IN"
inp_domain_cfg_file = "DOMCFG_IN"
outfile = "RNF_OUT_MOTHER"
verb = LVERB
# Open files
inp_rnf_2D = xr.open_dataset(rnf_inp_file)
inp_domain_cfg = xr.open_dataset(
    inp_domain_cfg_file,
    drop_variables={
        "x",
        "y",
    },
)
e1e2t = inp_domain_cfg.e1t.squeeze().values * inp_domain_cfg.e2t.squeeze().values

# Open variables
mask_inp_tmp = inp_domain_cfg.top_level.squeeze()  # [:,600:700]
mask_inp = np.where(mask_inp_tmp > 0.0, 1.0, 0.0)
rnf_2Dt = inp_rnf_2D.runoffs_instant.squeeze() * e1e2t[:, :]  # [:,:,600:700]

rnf_2Dt_new = np.zeros(rnf_2Dt.shape)
rnf_2Dt_new2 = np.zeros(rnf_2Dt.shape)
rnf_point = np.array(
    np.where(rnf_2Dt[0, :, :].values > 0)
)  # Assuming runoffs does not move

# 1 - Move runoffs the closest point near coast
print("STEP 1 : Move runoffs the closest point near coast")

rnf_2Dt_new[:, :, :] = move_runoffs(rnf_2Dt[:, :, :].values, rnf_point, mask_inp, verb)

# 2 - lay off the runoffs along coast (optional, but fancier)
print("STEP 2 : cosmetics")

rnf_point = np.array(
    np.where(rnf_2Dt_new[0, :, :] > 0)
)  # Assuming runoffs does not move

rnf_2Dt_new2[:, :, :] = move_runoffs_ij(
    rnf_2Dt_new[:, :, :], rnf_point, mask_inp, verb
)  # Just to check
rnf_2Dt_new2 = rnf_2Dt_new2 / e1e2t[:, :]

############################ Save in a Netcdf ###################################
rnf_2Dt_daily_new_da = xr.DataArray(
    data=rnf_2Dt_new2,
    dims=["time_counter", "y", "x"],
    coords=rnf_2Dt.coords,
    attrs=rnf_2Dt.attrs,
    name=rnf_2Dt.name,
)
rnf_2Dt_daily_new_da.to_netcdf(outfile, mode="w")

print("Computing sum (on first time_step)")
print("original file")
print(np.nansum(inp_rnf_2D.runoffs_instant.squeeze()[0, :, :] * e1e2t))
print(np.nansum(rnf_2Dt[0, :, :]))
print("After Step 1")
print(np.nansum(rnf_2Dt_new[0, :, :]))
print("After Step 2")
print(np.nansum(rnf_2Dt_new2[0, :, :] * e1e2t))
