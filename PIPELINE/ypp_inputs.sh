#!/bin/bash

# a simple file containing the participants to be analyzed

## Directories ##
DIR_PIPE='/srv/CODE/PIPELINE'
DIR_DATA='/srv/MRI/WORKING'
DIR_AFNI='/usr/local/abin'
DATA_TYPE='TASK'

AFNI_DECONFLICT=OVERWRITE

DIR_EXPT="TRSE"
SUBJECTS="1101 1103 1104 1202 1205 1208 1209 1210 1212 1214 1220 1223 \
          1306 1307 1309 1310 1311 1313 1314 1318 1325 1326 1328 1329 \
          1331 1332 1333 1336 1337 1338 1339 1340 1341 1342 1343 1344 \
          1346 1347 1349 1350"

#DIR_EXPT="SAB1"
#SUBJECTS="0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012"

#DIR_EXPT="ATOL"
#SUBJECTS="301 302 304 305 307 308 309 311 312 316 317 319 320 321 322 323 \
#          324 401 403 404 405 407 408 409 411 412 413 414 415 416 418 420"

#DIR_EXPT="TRSE_ENHANCE"
#SUBJECTS="700 701 702 703 704 705 706 707 708 709 710 711 712"

# DIR_EXPT="RSFC1"
# SUBJECTS="0023 0024 0025 0028 0029 0030 0031 0033 0034 0035 0036 0037 \
#           0038 0039 0040 0041 0042 0043 0044 0046 0047 0048 0050 0051 \
#           0052 0054 0055 0058 0060 0061 0062 0064 0065 0066 0067 0068 \
#           0070 0071 0072 0073 0074 0075 0076 0077 0078 0079 0081 0082 \
#           0083 0084"

#DIR_EXPT="BEBASD"
#SUBJECTS="101 102 103 105 106 107 108 201 202 203 204 205 206 207 209 211 212 213 214"
#SUBJECTS="106 107 205"

## Options
DELTR=0     # number of TRs to delete from the beginning of each run
DIMS=3.5      # set voxel dimensions post-reslice (iso)
POLORT=4    # degree of legendre polynomials to detrend data against
BLUR_FWHM=6 # blur FWHM

export DIR_PIPE
export DIR_DATA
export DIR_AFNI
export DATA_TYPE
export AFNI_DECONFLICT
export DIR_EXPT
export SUBJECTS
export DELTR
export DIMS
export POLORT
export BLUR_FWHM

# pipeline
#python PRE/freesurfer_T1_export.py
#./PRE/motioncorrect.sh
#./PRE/linreg_calculate.sh
#./PRE/linreg_FSATLAS_to_EPI.sh
#./PRE/create_regressors.sh
#./PRE/filter.sh
#./PRE/linreg_EPI_to_MNI.sh

#./UTIL/cleanup_functionals.sh
./UTIL/check_runs.sh