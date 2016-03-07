#!/usr/bin/env python
"""
Projects a volume result to a surface of visulatization

Usage:
  project-vol-to-cifti-forvis.py [options] <vol.nii.gz> <hcp_subject_dir> <output.dscalar.nii>

Arguments:
    <vol.nii.gz>           Nifty volume to project to cifti space
    <hcp_subject_dir>      Path to the hcp subject directory
    <output.dscalar.nii>   Output dscalar.nii image

Options:
  -v,--verbose             Verbose logging
  --debug                  Debug logging in Erin's very verbose style
  -n,--dry-run             Dry run
  -h,--help                Print help

DETAILS
This projects to the MNINonLinear/32k_fs_LR space in hcp for this subject
(the space used for fMRI analysis) With no real smoothing in the subcortical space

This is good for converting a final result for visualization.
For an analysis you probably want a fancier algoritm from the HCP pipeline

Written by Erin W Dickie, Jan 7, 2016
"""
from docopt import docopt
import numpy as np
import nibabel as nib
import os
import tempfile
import shutil
import subprocess
import pandas as pd

arguments       = docopt(__doc__)
input_nii          = arguments['<vol.nii.gz>']
hcp_subject_dir = arguments['<hcp_subject_dir>']
output_dscalar  = arguments['<output.dscalar.nii>']
VERBOSE         = arguments['--verbose']
DEBUG           = arguments['--debug']
DRYRUN          = arguments['--dry-run']

###
### Erin's little function for running things in the shell
def docmd(cmdlist):
    "sends a command (inputed as a list) to the shell"
    if DEBUG: print ' '.join(cmdlist)
    if not DRYRUN: subprocess.call(cmdlist)

#mkdir a tmpdir for the
tmpdir = tempfile.mkdtemp()

subject = os.path.basename(hcp_subject_dir)

## project to Left surface template
docmd(['wb_command',
    '-volume-to-surface-mapping',
    input_nii,
    os.path.join(hcp_subject_dir,'MNINonLinear','fsaverage_LR32k', subject + '.L.midthickness.32k_fs_LR.surf.gii'),
    os.path.join(tmpdir, 'L.func.gii'),
    '-ribbon-constrained',
    os.path.join(hcp_subject_dir,'MNINonLinear','fsaverage_LR32k', subject + '.L.white.32k_fs_LR.surf.gii'),
    os.path.join(hcp_subject_dir,'MNINonLinear','fsaverage_LR32k', subject + '.L.pial.32k_fs_LR.surf.gii')])


## project to Right surface template
docmd(['wb_command',
    '-volume-to-surface-mapping',
    input_nii,
    os.path.join(hcp_subject_dir,'MNINonLinear','fsaverage_LR32k', subject + '.R.midthickness.32k_fs_LR.surf.gii'),
    os.path.join(tmpdir, 'R.func.gii'),
    '-ribbon-constrained',
    os.path.join(hcp_subject_dir,'MNINonLinear','fsaverage_LR32k', subject + '.R.white.32k_fs_LR.surf.gii'),
    os.path.join(hcp_subject_dir,'MNINonLinear','fsaverage_LR32k', subject + '.R.pial.32k_fs_LR.surf.gii')])

## chop out the subcortical structures
docmd(['wb_command',
    '-volume-parcel-resampling',
    input_nii,
    os.path.join(hcp_subject_dir,'MNINonLinear','ROIs','ROIs.2.nii.gz'),
    os.path.join(hcp_subject_dir,'MNINonLinear','ROIs','Atlas_ROIs.2.nii.gz'),
    '2',
    os.path.join(tmpdir, 'AtlasSubcortical.nii.gz')])

## combind all three into a dscalar..
docmd(['wb_command',
    '-cifti-create-dense-scalar',
    output_dscalar,
    '-volume',
    os.path.join(tmpdir, 'AtlasSubcortical.nii.gz'),
    os.path.join(hcp_subject_dir,'MNINonLinear','ROIs','Atlas_ROIs.2.nii.gz'),
    '-left-metric',
    os.path.join(tmpdir, 'L.func.gii'),
    '-roi-left',
    os.path.join(hcp_subject_dir,'MNINonLinear','fsaverage_LR32k',subject + '.L.atlasroi.32k_fs_LR.shape.gii'),
    '-right-metric',
    os.path.join(tmpdir, 'R.func.gii'),
    '-roi-right',
     os.path.join(hcp_subject_dir,'MNINonLinear','fsaverage_LR32k',subject + '.R.atlasroi.32k_fs_LR.shape.gii')])

#get rid of the tmpdir
shutil.rmtree(tmpdir)
