#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import xarray as xr
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import shutil
from shutil import copyfile
import time


######################################################################################################################
def check_mask_nearby_ij(i,j,mask,ndist):
    # i = index along i of point to test
    # j = index along j of point to test
    # mask = 2D mask 
    # ndist = distance from center to check
    if (i > (ndist-1)):
        TEST_i = np.nansum(mask[i-ndist:i+ndist+1,j])
    else:
        TEST_i = np.nansum(mask[i:i+ndist+1,j])
    if (j > (ndist-1)):
        TEST_j = np.nansum(mask[i,j-ndist:j+ndist+1])
    else:
        TEST_j = np.nansum(mask[i,j:j+ndist+1])
    return TEST_i, TEST_j    


######################################################################################################################
def get_npoints_ij(i,j,mask,ndist,rnf_data):
        # return the number of sea points at ndist distance
        arr= np.array([rnf_data[i-ndist,j] + mask[i-ndist,j],\
                     rnf_data[i+ndist,j]    + mask[i+ndist,j],\
                     rnf_data[i,j-ndist]   + mask[i,j-ndist], \
                     rnf_data[i,j+ndist]   + mask[i,j+ndist]])
        ind=np.array(np.argwhere(arr==0))
        if len(ind>0):
            return len(ind)
        else:
            ind=np.array(np.argwhere(arr<1))
            return len(ind)


######################################################################################################################
def check_if_surrounded_by_land(i,j,mask,ndist):
    surrounded_by_land=0
    dim_i , dim_j =int(len(mask[:,0])),int(len(mask[0,:]))
    # i = index along i of point to test
    # j = index along j of point to test
    # mask = 2D mask 
    # ndist = distance from center to check
    if (i > (ndist-1)):
        if (j > (ndist-1)):
            npts = np.nansum(mask[i-ndist:i+ndist+1,j-ndist:j+ndist+1])
            if npts == (1+(ndist*2))**2 :
                surrounded_by_land=1
        else:
            npts = np.nansum(mask[i-ndist:i+ndist+1,j:j+ndist+1])
            if npts == (1+(ndist*2))*(1+(ndist*2)-ndist) :
                surrounded_by_land=1
    else:
        if (j > (ndist-1)):
            npts = np.nansum(mask[i:i+ndist+1,j-ndist:j+ndist+1])
            if npts == (1+(ndist*2))*(1+(ndist*2)-ndist):
                surrounded_by_land=1
        else:
            npts = np.nansum(mask[i:i+ndist+1,j:j+ndist+1])
            if npts == (1+(ndist*2)-ndist)*(1+(ndist*2)-ndist) :
                surrounded_by_land=1

    if (i < ((dim_i-1) - ndist)):
        if (j < ((dim_j-1) - ndist)):
            npts = np.nansum(mask[i-ndist:i+ndist+1,j-ndist:j+ndist+1])
            if npts == (1+(ndist*2))**2 :
                surrounded_by_land=1
        else:
            npts = np.nansum(mask[i-ndist:i+ndist+1,j-ndist:j+1])
            if npts == (1+(ndist*2))*(1+(ndist*2)-ndist) :
                surrounded_by_land=1
    else:
        if (j < ((dim_j-1) - ndist)):
            npts = np.nansum(mask[i-ndist:i+ndist+1,j-ndist:j+ndist+1])
            if npts == (1+(ndist*2))*(1+(ndist*2)-ndist):
                surrounded_by_land=1
        else:
            npts = np.nansum(mask[i-ndist:i+1,j-ndist:j+ndist])
            if npts == (1+(ndist*2)-ndist)*(1+(ndist*2)-ndist) :
                surrounded_by_land=1
    return surrounded_by_land 


######################################################################################################################
def check_if_surrounded_by_sea(i,j,mask,ndist,nseuil):
    mask_inv=np.where(mask==1,0,1)
    surrounded_by_sea=0
    dim_i , dim_j =int(len(mask_inv[:,0])),int(len(mask_inv[0,:]))
    # i = index along i of point to test
    # j = index along j of point to test
    # mask_inv = 2D mask_inv 
    # ndist = distance from center to check
    if (i > (ndist-1)):
        if (j > (ndist-1)):
            npts = np.nansum(mask_inv[i-ndist:i+ndist+1,j-ndist:j+ndist+1])
            if npts == (1+(ndist*2))**2 :
                surrounded_by_sea=1
        else:
            npts = np.nansum(mask_inv[i-ndist:i+ndist+1,j:j+ndist+1])
            if npts == (1+(ndist*2))*(1+(ndist*2)-ndist) :
                print(npts)
                surrounded_by_sea=1
    else:
        if (j > (ndist-1)):
            npts = np.nansum(mask_inv[i:i+ndist+1,j-ndist:j+ndist+1])
            if npts == (1+(ndist*2))*(1+(ndist*2)-ndist):
                surrounded_by_sea=1
        else:
            npts = np.nansum(mask_inv[i:i+ndist+1,j:j+ndist+1])
            if npts == (1+(ndist*2)-ndist)*(1+(ndist*2)-ndist) :
                surrounded_by_sea=1

    if (i < ((dim_i-1) - ndist)):
        if (j < ((dim_j-1) - ndist)):
            npts = np.nansum(mask_inv[i-ndist:i+ndist+1,j-ndist:j+ndist+1])
            if npts == (1+(ndist*2))**2 :
                surrounded_by_sea=1
        else:
            npts = np.nansum(mask_inv[i-ndist:i+ndist+1,j-ndist:j+ndist])
            if npts == (1+(ndist*2))*(1+(ndist*2)-ndist) :
                surrounded_by_sea=1
    else:
        if (j < ((dim_j-1) - ndist)):
            npts = np.nansum(mask_inv[i-ndist:i+ndist,j-ndist:j+ndist+1])
            if npts == (1+(ndist*2))*(1+(ndist*2)-ndist):
                surrounded_by_sea=1
        else:
            npts = np.nansum(mask_inv[i-ndist:i+ndist,j-ndist:j+ndist])
            if npts == (1+(ndist*2)-ndist)*(1+(ndist*2)-ndist) :
                surrounded_by_sea=1
    return surrounded_by_sea 


######################################################################################################################
def find_nearest_sea_point(i,j,mask,ndist,rnf_data):
    i_ind_new=[]
    j_ind_new=[]
    
# First, check along i / j only
    if (i > (ndist-1)):
        if (j > (ndist-1)):
            arr = rnf_data[i-ndist:i+ndist+1,j-ndist:j+ndist+1] + mask[i-ndist:i+ndist+1,j-ndist:j+ndist+1]
        else:
            arr = rnf_data[i-ndist:i+ndist+1,j:j+ndist+1] + mask[i-ndist:i+ndist+1,j:j+ndist+1]
    else:
        if (j > (ndist-1)):
            arr = rnf_data[i:i+ndist+1,j-ndist:j+ndist+1] + mask[i:i+ndist+1,j-ndist:j+ndist+1]
        else:
            arr = rnf_data[i:i+ndist+1,j:j+ndist+1] + mask[i:i+ndist+1,j:j+ndist+1]
   
    available_points_all=np.argwhere(arr[:,:]==0)  - ndist
    available_points_all[:,0]=available_points_all[:,0] + i 
    available_points_all[:,1]=available_points_all[:,1] + j  
# First, check if there is an empty point around
    arr_ij=np.ones(arr.shape)
    if 0 in arr:
        # check along i and j axis only
        arr_ij[ndist,:]=arr[ndist,:]
        arr_ij[:,ndist]=arr[:,ndist]
        available_points_ij=np.argwhere(arr_ij[:,:]==0) - ndist
        available_points_ij[:,0]=available_points_ij[:,0] + i 
        available_points_ij[:,1]=available_points_ij[:,1] + j 
    if 0 in arr_ij :
        return available_points_ij
    else: # If no empty point, return the closests sea points
        
        if (i > (ndist-1)):
            if (j > (ndist-1)):
                arr = mask[i-ndist:i+ndist+1,j-ndist:j+ndist+1]
            else:
                arr = mask[i-ndist:i+ndist+1,j:j+ndist+1]
        else:
            if (j > (ndist-1)):
                arr = mask[i:i+ndist+1,j-ndist:j+ndist+1]
            else:
                arr = mask[i:i+ndist+1,j:j+ndist+1]  
                
        available_points_all=np.argwhere(arr[:,:]==0)  - ndist
        available_points_all[:,0]=available_points_all[:,0] + i 
        available_points_all[:,1]=available_points_all[:,1] + j  
        if 0 in arr:
            arr_ij=np.ones(arr.shape)
            arr_ij[ndist,:]=arr[ndist,:]
            arr_ij[:,ndist]=arr[:,ndist]
            available_points_ij=np.argwhere(arr_ij[:,:]==0)  - ndist
            available_points_ij[:,0]=available_points_ij[:,0] + i 
            available_points_ij[:,1]=available_points_ij[:,1] + j 
            if 0 in arr_ij :
                return available_points_ij
            else:
                return available_points_all
            del(available_points_all, available_points_ij)
        else:
            print("ERROR")
            print(arr)


######################################################################################################################
def get_nearest_coast_point(i,j,ndist,arr):
    available_points_all=np.argwhere(arr[:,:]==0)
    if i < (ndist - 1):
        if j< (ndist - 1):
            available_points_all[:,0]=available_points_all[:,0] + i - (ndist - 1)
            available_points_all[:,1]=available_points_all[:,1] + j - (ndist - 1) 
            available_points_all[:,0]=np.where(available_points_all[:,0]>i,available_points_all[:,0]-1,available_points_all[:,0])
            available_points_all[:,1]=np.where(available_points_all[:,1]>j,available_points_all[:,1]-1,available_points_all[:,1])             
        else:       
            available_points_all[:,0]=available_points_all[:,0] + i - (ndist - 1)
            available_points_all[:,1]=available_points_all[:,1] + j - ndist
            available_points_all[:,0]=np.where(available_points_all[:,0]<i,available_points_all[:,0]+1,available_points_all[:,0])
            available_points_all[:,0]=np.where(available_points_all[:,0]>i,available_points_all[:,0]-1,available_points_all[:,0])
            available_points_all[:,1]=np.where(available_points_all[:,1]<j,available_points_all[:,1]+1,available_points_all[:,1])
            available_points_all[:,1]=np.where(available_points_all[:,1]>j,available_points_all[:,1]-1,available_points_all[:,1])
    else:   
        available_points_all[:,0]=available_points_all[:,0] + i - ndist 
        available_points_all[:,1]=available_points_all[:,1] + j - ndist
        available_points_all[:,0]=np.where(available_points_all[:,0]<i,available_points_all[:,0]+1,available_points_all[:,0])
        available_points_all[:,0]=np.where(available_points_all[:,0]>i,available_points_all[:,0]-1,available_points_all[:,0])
        available_points_all[:,1]=np.where(available_points_all[:,1]<j,available_points_all[:,1]+1,available_points_all[:,1])
        available_points_all[:,1]=np.where(available_points_all[:,1]>j,available_points_all[:,1]-1,available_points_all[:,1])

    return(available_points_all)


######################################################################################################################
def find_nearest_coast_point(i,j,mask,ndist,rnf_data):
    mask_inv=np.where(mask==1,0,1)
    i_ind_new=[]
    j_ind_new=[]
    idim ,jdim = int(len(mask[:,0])), int(len(mask[0,:]))
# First, check if there is an empty point around    
    if (i > (ndist-1)):
        if (j > (ndist-1)):
            arr = rnf_data[i-ndist:i+ndist+1,j-ndist:j+ndist+1] + mask_inv[i-ndist:i+ndist+1,j-ndist:j+ndist+1]
        else:
            arr = rnf_data[i-ndist:i+ndist+1,j:j+ndist+1] + mask_inv[i-ndist:i+ndist+1,j:j+ndist+1]
    else:
        if (j > (ndist-1)):
            arr = rnf_data[i:i+ndist+1,j-ndist:j+ndist+1] + mask_inv[i:i+ndist+1,j-ndist:j+ndist+1]
        else:
            arr = rnf_data[i:i+ndist+1,j:j+ndist+1] + mask_inv[i:i+ndist+1,j:j+ndist+1]

    arr_ij=np.ones(arr.shape)
    if 0 in arr:
        arr_ij[ndist,:]=arr[ndist,:]
        arr_ij[:,ndist]=arr[:,ndist]
    if 0 in arr_ij :
        # check along i and j axis only
        available_points = get_nearest_coast_point(i,j,ndist,arr_ij)
    
# Then, if no empty point, return the closests sea points
    else: 
        
        if (i > (ndist-1)):
            if (j > (ndist-1)):
                arr = mask_inv[i-ndist:i+ndist+1,j-ndist:j+ndist+1]
            else:
                arr = mask_inv[i-ndist:i+ndist+1,j:j+ndist+1]
        else:
            if (j > (ndist-1)):
                arr = mask_inv[i:i+ndist+1,j-ndist:j+ndist+1]
            else:
                arr = mask_inv[i:i+ndist+1,j:j+ndist+1]  
        if 0 in arr:
            arr_ij=np.ones(arr.shape)
            arr_ij[ndist,:]=arr[ndist,:]
            arr_ij[:,ndist]=arr[:,ndist]
            if 0 in arr_ij :
                # check along i and j axis only
                available_points = get_nearest_coast_point(i,j,ndist,arr_ij)
            else:
                available_points = get_nearest_coast_point(i,j,ndist,arr)
        else:
            print("ERROR")
            print(arr)
    return available_points


######################################################################################################################
def move_runoffs(rnf_2Dt,rnf_point,mask,verb):
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
    nseuil=30 # over 30 points distance, do not replace runoff
    rnf_2D=rnf_2Dt[0,:,:]
    rnf_2Dt_new = np.copy(rnf_2Dt)
#     rnf_2Dt_new[:,:,:] = 0.

    mask_data=mask
    mask_data=np.where(mask_data==1,0,1) # invert mask
    sea_point_not_found=0.
    land_point_not_found=0.
    ndist=1
    
# --------------------------------------------------------------------------------------------------
# BEGIN LOOP
    print(len(rnf_point[0,:]))
# Loop over valid runoff values only  
    for n in range(len(rnf_point[0,:])): 
        print("treating runoff point ",rnf_point[0,n],rnf_point[1,n], n, "/", len(rnf_point[0,:]))
        
        if (mask_data[rnf_point[0,n],rnf_point[1,n]]==1): # POINT IS OVER LAND ------------
            surrounded = check_if_surrounded_by_land(rnf_point[0,n], \
                         rnf_point[1,n],mask_data,ndist)
            if verb: print("==> j, i = ", rnf_point[0,n],rnf_point[1,n],"is on mask point")

            if surrounded == 1: # Surrounded by earth
                if (ndist > nseuil): 
                    if verb: print("WARNING !!! : closest sea point is over ",nseuil,\
			      "point perimeter at i, j = ", rnf_point[0,n],rnf_point[1,n])

                while sea_point_not_found == 0:
                    surrounded = check_if_surrounded_by_land(rnf_point[0,n], rnf_point[1,n],mask_data,ndist)

                    if surrounded == 1: # No sea point in ndist perimeter 
                        if verb: print(rnf_point[0,n],rnf_point[1,n],"surrounded by earth points, trying ndist=+1;",\
                                              "next radius = ", (1+((ndist+1)*2)))
                    else: # At least one sea point in ndist perimeter
                        sea_point_not_found=1.
                        indexes_closests_sea_point=find_nearest_sea_point(rnf_point[0,n],rnf_point[1,n],\
                                                               mask_data,ndist,rnf_2D)
                    ndist=ndist+1
  
            else: # AT LEAST ONE SEA POINT in ndist=1 perimeter ------------
                indexes_closests_sea_point=find_nearest_sea_point(rnf_point[0,n],rnf_point[1,n],mask_data,\
                                                     ndist,rnf_2D)
    # NOW REPLACE RUNOFFS
            npoints=len(indexes_closests_sea_point[:,0])
            # Now replace data
            if npoints == 0: 
                # No available points nearby without an already existing runoff value => avoid
                #rnf_2Dt_new[:,rnf_point[0,n],rnf_point[1,n]] = 0.  
                print(rnf_point[0,n],rnf_point[1,n],"ISSUE AT THIS POINT !!")
            else: 
                for ind in range(npoints):
                    if verb: print("moving point over ", npoints, "points : i,j ",ind + 1, "/",npoints, ":"\
                        ,"=",int(indexes_closests_sea_point[ind,0]),int(indexes_closests_sea_point[ind,1])  ) 
                    rnf_2Dt_new[:,rnf_point[0,n],rnf_point[1,n]]=0.
                    rnf_2Dt_new[:,int(indexes_closests_sea_point[ind,0]),int(indexes_closests_sea_point[ind,1])]\
                     = rnf_2Dt_new[:,int(indexes_closests_sea_point[ind,0]),int(indexes_closests_sea_point[ind,1])]\
                        + (rnf_2Dt[:,rnf_point[0,n],rnf_point[1,n]] / npoints) 
                    

        else: #POINT IS OVER SEA ------------
            ndist=1
            surrounded = check_if_surrounded_by_sea(rnf_point[0,n], \
                                                   rnf_point[1,n],mask_data,ndist,3)
            # Loop until we find at least one sea point in ndist perimeter$
            if surrounded == 1: # Surrounded by sea
                if verb: 
                    print("==> j, i = ", rnf_point[0,n],rnf_point[1,n],\
                                                    "is surrounded by sea ")
                if (ndist > nseuil): 
                    print("WARNING !!! : closest land point is over ",nseuil,\
                       	"point perimeter at i, j = ", rnf_point[0,n],rnf_point[1,n])

                while land_point_not_found == 0:
                        surrounded = check_if_surrounded_by_sea(rnf_point[0,n],\
                                                               rnf_point[1,n],mask_data,ndist,3)
                        
                        if surrounded == 1: # No sea point in ndist perimeter 
                            if verb: print(rnf_point[0,n],rnf_point[1,n],\
                                            "surrounded by sea points, trying ndist=+1;",\
                                                  "next radius = ", (1+((ndist+1)*2)))
                        else: # At least one sea point in ndist perimeter
                            land_point_not_found=1.
                            indexes_closests_land_point=find_nearest_coast_point(rnf_point[0,n],rnf_point[1,n],\
                                                                   mask_data,ndist,rnf_2D)
                      
                        ndist=ndist+1
    # NOW REPLACE RUNOFFS
                npoints=len(indexes_closests_land_point[:,0])
                # Now replace data
                if npoints == 0: 
                    # No available points nearby without an already existing runoff value => avoid
                    #rnf_2Dt_new[:,rnf_point[0,n],rnf_point[1,n]] = 0.  
                    print(rnf_point[0,n],rnf_point[1,n],"ISSUE AT THIS POINT !!")
                else: 
                    for ind in range(npoints):
                        print(ind)
                        if verb: print("moving point over ", npoints, "points, : i, j =",\
                                 int(indexes_closests_land_point[ind,0]),int(indexes_closests_land_point[ind,1])  )                                      
                        rnf_2Dt_new[:,rnf_point[0,n],rnf_point[1,n]]=0.
                        rnf_2Dt_new[:,int(indexes_closests_land_point[ind,0]),int(indexes_closests_land_point[ind,1])]= \
			rnf_2Dt_new[:,int(indexes_closests_land_point[ind,0]),int(indexes_closests_land_point[ind,1])]  \
                          + (rnf_2Dt[:,rnf_point[0,n],rnf_point[1,n]] / npoints) 
        sea_point_not_found=0.
        land_point_not_found=0.
        ndist=1

    if verb: print("..........")

        # Next point
    return rnf_2Dt_new
# --------------------------------------------------------------------------------------------------
# END LOOP


######################################################################################################################
def find_nearest_coast_point_ij(i,j,mask,rnf_data,nseuil):
    out=[]
    n=1
    var=0
    nip1,nim1,njp1,njm1 = 0 ,0 ,0 ,0 
    while (var==0) and (n<nseuil):
        if mask[i+n,j]==1:
            if (rnf_data[i+n-1,j] == 0.):
                if (mask[i+n-1,j] == 0.):
                    out=np.append(out,[i+n-1,j])
                else:
                    nip1=1
        if mask[i-n,j]==1:
            if (rnf_data[i-n+1,j] == 0.): 
                if (mask[i-n+1,j] == 0.):
                    out=np.append(out,[i-n+1,j])
                else:
                    nim1=1
        if mask[i,j+n]==1:
            if (rnf_data[i,j+n-1] == 0.):
                if (mask[i,j+n-1] == 0.):
                    out=np.append(out,[i,j+n-1])
                else:
                    njp1=1
        if mask[i,j-n]==1:
            if (rnf_data[i,j-n+1] == 0.): 
                if (mask[i,j-n+1] == 0.):
                    out=np.append(out,[i,j-n+1])  
                else:
                    njm1=1
           
        var=len(out)
        if var==0: # In case we have gone too far
            if nip1==1: out=np.append(out,[i+n-2,j])
            if nim1==1: out=np.append(out,[i-n+2,j])
            if njp1==1: out=np.append(out,[i,j+n-2])
            if njm1==1: out=np.append(out,[i,j-n+2]) 
        n=n+1
        var=len(out)
         
    return(out) # closest coastal point
        


######################################################################################################################
def move_runoffs_ij(rnf_2D,rnf_point,mask,verb):
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
    nseuil=4 # over 4 points distance, do not replace runoff
    rnf_2D_new = np.copy(rnf_2D)
    mask_data=mask
    mask_data=np.where(mask_data==1,0,1) # invert mask
    sea_point_not_found=0.
    ndist=1
    
# --------------------------------------------------------------------------------------------------
# BEGIN LOOP

# Loop over valid runoff values only  
    for n in range(len(rnf_point[0,:])): 
        N_earth_points_i, N_earth_points_j = check_mask_nearby_ij(rnf_point[0,n],  \
                                             rnf_point[1,n],mask_data,ndist)
        N_earth_points_ij = N_earth_points_i + N_earth_points_j
        if(N_earth_points_ij > 0): # at least one earth point nearby
            if verb: print("==> j, i = ", rnf_point[0,n],rnf_point[1,n], "ok")
                    

# POINT IS SURROUNDED BY SEA along i and j------------
        else: # no earth point nearby

            if verb: print(rnf_point[0,n],rnf_point[1,n], "is in the middle of the sea", \
                            N_earth_points_i, N_earth_points_j,mask_data[rnf_point[0,n]+1,rnf_point[1,n]])
            # ------------------------------------------------
            # Find nearest coast point from 1 to nseuil distance
            ind = find_nearest_coast_point_ij(rnf_point[0,n],rnf_point[1,n],mask_data,rnf_2D,nseuil)
            npoints=len(ind)/2
            # ------------------------------------------------
                      
            if npoints == 0: # No available points nearby without an already existing runoff value => avoid
                #rnf_2D_new[rnf_point[0,n],rnf_point[1,n]] = 0.  
                print("WARNING : point at i, j = ", rnf_point[0,n],rnf_point[1,n] ,                                    " is way too far from coast => ignore")
            if npoints == 1: 
                rnf_2D_new[int(ind[0]),int(ind[1])] = rnf_2D_new[int(ind[0]),int(ind[1])]                        + rnf_2D_new[rnf_point[0,n],rnf_point[1,n]]
                rnf_2D_new[rnf_point[0,n],rnf_point[1,n]] = 0.   
                if verb: print("moving point j,i = ", rnf_point[0,n],rnf_point[1,n],                                            "at point j,i = ", ind)
            if npoints == 2: 
                rnf_2D_new[int(ind[0]),int(ind[1])] = rnf_2D_new[int(ind[0]),int(ind[1])]                        + (rnf_2D_new[rnf_point[0,n],rnf_point[1,n]] / 2) 
                rnf_2D_new[int(ind[2]),int(ind[3])] = rnf_2D_new[int(ind[2]),int(ind[3])]                        + (rnf_2D_new[rnf_point[0,n],rnf_point[1,n]] / 2 )
                rnf_2D_new[rnf_point[0,n],rnf_point[1,n]] = 0. 
                if verb: print("dispatch point j,i = ", rnf_point[0,n],rnf_point[1,n],                                "at 2 points j1,i1,j2,i2 = ", ind)
            if npoints > 2: print("OVER 2")
            if verb: print("..........")

        sea_point_not_found=0.
        ndist=1
        # Next point
    return rnf_2D_new
# --------------------------------------------------------------------------------------------------
# END LOOP


######################################################################################################################
# MAIN PROGRAM #
######################################################################################################################

year=2018

rnf_inp_file='RNF_IN'
inp_domain_cfg_file='DOMCFG_IN'
outfile='RNF_OUT_MOTHER'
verb=LVERB
# Open files
inp_rnf_2D=xr.open_dataset(rnf_inp_file)
inp_domain_cfg=xr.open_dataset(inp_domain_cfg_file,drop_variables={"x", "y",})
e1e2t= inp_domain_cfg.e1t.squeeze().values * inp_domain_cfg.e2t.squeeze().values

# Open variables
mask_inp_tmp =  inp_domain_cfg.top_level.squeeze() #[:,600:700]
mask_inp = np.where(mask_inp_tmp > 0., 1., 0.)
rnf_2Dt=inp_rnf_2D.runoffs_instant.squeeze() * e1e2t[:,:] #[:,:,600:700]
rnf_2Dt_new=np.zeros(rnf_2Dt.shape)
rnf_2Dt_new2=np.zeros(rnf_2Dt.shape)
rnf_point = np.array(np.where(rnf_2Dt[0,:,:].values>0)) # Assuming runoffs does not move

# 1 - Move runoffs the closest point near coast
print("STEP 1 : Move runoffs the closest point near coast")

rnf_2Dt_new[:,:,:]=move_runoffs(rnf_2Dt[:,:,:].values,rnf_point,mask_inp,verb)

# 2 - lay off the runoffs along coast (optional, but fancier)
print("STEP 2 : cosmetics")

rnf_point = np.array(np.where(rnf_2Dt_new[0,:,:]>0)) # Assuming runoffs does not move
for i in range(len(rnf_2Dt_new[:,0,0])):
    print("STEP 2 : processing time_step :",  i)
    
    rnf_2Dt_new2[i,:,:]=move_runoffs_ij(rnf_2Dt_new[i,:,:],rnf_point,mask_inp,verb) # Just to check
rnf_2Dt_new2 = rnf_2Dt_new2 / e1e2t[:,:]

# Date variables ----------------------------------------------------------------------------------------
dstart_year= str(year) + "-01-01" # 1st day of the year
dend_year= str(year) + "-12-31" # last day of the year

dstart_clim_monthly = str(year) + "-01-15" # for 12 month clim
dend_clim_monthly = str(year) + "-12-15" # for 12 month clim
dstart_minus_1_month = str(year-1) + "-12-01" # used for conversion from monthly to daily clim data

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
print(np.nansum(inp_rnf_2D.runoffs_instant.squeeze()[0,:,:] *e1e2t))
print("After Step 1")
print(np.nansum(rnf_2Dt_new[0,:,:] ) )
print("After Step 2")
print(np.nansum(rnf_2Dt_new2[0,:,:] *e1e2t) )


