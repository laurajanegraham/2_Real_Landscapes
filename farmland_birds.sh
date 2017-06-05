#!/bin/bash

#PBS -N fb_real
#PBS -l walltime=00:60:00
#PBS -t 1-746

cd $PBS_O_WORKDIR

# set to work in the conda environment with the correct packages installed
export PATH="/home/lg1u16/miniconda2/bin:$PATH"

python farmland_birds.py
