#!/bin/bash

#PBS -N farmland_birds_real
#PBS -l walltime=00:30:00
#PBS -t 1-746

cd $PBS_O_WORKDIR

python farmland_birds.py
