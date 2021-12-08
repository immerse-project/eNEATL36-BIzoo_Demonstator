MODULE usrdef_istate
   !!==============================================================================
   !!                       ***  MODULE usrdef_istate  ***
   !!
   !!                        ===  TEST configuration  ===
   !!
   !! User defined : set the initial state of a user configuration
   !!==============================================================================
   !! History :  NEMO 4.x ! 2020-12  (J. Chanut) Original code
   !!----------------------------------------------------------------------

   !!----------------------------------------------------------------------
   !!  usr_def_istate : initial state in Temperature and salinity
   !!----------------------------------------------------------------------
   USE par_oce        ! ocean space and time domain
   USE phycst         ! physical constants
   USE eosbn2, ONLY: rn_a0
   USE dom_oce
   !
   USE in_out_manager ! I/O manager
   USE lib_mpp        ! MPP library
   
   IMPLICIT NONE
   PRIVATE

   PUBLIC   usr_def_istate   ! called by istate.F90
   PUBlIC   usr_def_istate_ssh
   !!----------------------------------------------------------------------
   !! NEMO/OCE 4.0 , NEMO Consortium (2018)
   !! $Id: usrdef_istate.F90 12489 2020-02-28 15:55:11Z davestorkey $ 
   !! Software governed by the CeCILL license (see ./LICENSE)
   !!----------------------------------------------------------------------
   !! * Substitutions
#  include "do_loop_substitute.h90"

CONTAINS
  
   SUBROUTINE usr_def_istate( pdept, ptmask, pts, pu, pv )
      !!----------------------------------------------------------------------
      !!                   ***  ROUTINE usr_def_istate  ***
      !! 
      !! ** Purpose :   Initialization of the dynamics and tracers
      !!                Here OVERFLOW configuration 
      !!
      !! ** Method  : - set temprature field
      !!              - set salinity   field
      !!
      !! ** Reference: Legg, S., Hallberg, R. W.  and J. B. Girton, 2006:
      !!               Comparison of entrainment in overflows simulated by z-coordinate,
      !!               isopycnal and non-hydrostatic models. Ocean Modelling, 11, 69-97.
      !!
      !!----------------------------------------------------------------------
      REAL(wp), DIMENSION(jpi,jpj,jpk)     , INTENT(in   ) ::   pdept   ! depth of t-point               [m]
      REAL(wp), DIMENSION(jpi,jpj,jpk)     , INTENT(in   ) ::   ptmask  ! t-point ocean mask             [m]
      REAL(wp), DIMENSION(jpi,jpj,jpk,jpts), INTENT(  out) ::   pts     ! T & S fields      [Celsius ; g/kg]
      REAL(wp), DIMENSION(jpi,jpj,jpk)     , INTENT(  out) ::   pu      ! i-component of the velocity  [m/s] 
      REAL(wp), DIMENSION(jpi,jpj,jpk)     , INTENT(  out) ::   pv      ! j-component of the velocity  [m/s] 
      !
      INTEGER  :: ji,jj,jk     ! dummy loop indices
      REAL(wp) :: zdt, zn2, zrho1, zdb, zh, zstar, zxw, zro, zhe, zh0, zf
      REAL(wp) :: zri1, zri2, zri, ztd, ztu
      !!----------------------------------------------------------------------
      !
      IF(lwp) WRITE(numout,*)
      IF(lwp) WRITE(numout,*) 'usr_def_istate : TEST configuration, analytical definition of initial state'
      IF(lwp) WRITE(numout,*) '~~~~~~~~~~~~~~   Ocean at rest, filled with a constant stratification '
      IF(lwp) WRITE(numout,*) '                 salinity is constant here' 
      !
      !
      pu  (:,:,:)  = 0._wp       ! ocean at rest
      pv  (:,:,:)  = 0._wp
      pts(:,:,:,:) = 0._wp
      !
      zn2 = (2.e-3)**2 ! brunt vaisala squared
      !                          ! T & S profiles
      DO_2D( 1, 1, 1, 1 )
         DO jk = 1, jpkm1
            zdt =  pdept(ji,jj,jk)
            zrho1 = rho0*zn2*zdt/grav/rn_a0
            pts(ji,jj,jk,jp_tem) = (15._wp - zrho1) * ptmask(ji,jj,jk)
! Mass conserving initialization:
!            ztd = 15._wp*gdepw_0(ji,jj,jk+1)-0.5*rho0*zn2/(rn_a0*grav)*gdepw_0(ji,jj,jk+1)**2
!            ztu = 15._wp*gdepw_0(ji,jj,jk  )-0.5*rho0*zn2/(rn_a0*grav)*gdepw_0(ji,jj,jk  )**2
!            pts(ji,jj,jk,jp_tem) = (ztd - ztu)/e3t_0(ji,jj,jk) * ptmask(ji,jj,jk)
            pts(ji,jj,jk,jp_sal) = 35._wp * ptmask(ji,jj,jk)
         END DO
      END_2D
      !   
   END SUBROUTINE usr_def_istate

  
   SUBROUTINE usr_def_istate_ssh( ptmask, pssh )
      !!----------------------------------------------------------------------
      !!                   ***  ROUTINE usr_def_istate  ***
      !! 
      !! ** Purpose :   Initialization of ssh
      !!                Here TEST configuration 
      !!
      !! ** Method  :   set no initial sea level anomaly
      !!  
      !!----------------------------------------------------------------------
      REAL(wp), DIMENSION(jpi,jpj,jpk)     , INTENT(in   ) ::   ptmask  !
      REAL(wp), DIMENSION(jpi,jpj)         , INTENT(  out) ::   pssh    !
      !
      !!----------------------------------------------------------------------
      !
      pssh(:,:) = 0._wp
      !
   END SUBROUTINE usr_def_istate_ssh

   !!======================================================================
END MODULE usrdef_istate
