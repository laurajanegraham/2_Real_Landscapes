# -*- coding: utf-8 -*-
"""
Created on Thu May 25 10:18:20 2017

@author: lg1u16
"""
# this is for calculating estimated species richness of farmland bird indicator species
# it needs properly sorting out for running on HPC

import nlmfunctions as nlm
import georasters as gr
import geopandas as gpd
import numpy as np
import pandas as pd
import uuid
from scipy.ndimage.filters import generic_filter

# we need the job ID from the HPC job array to select the correct grid cells
job_id = os.getenv('PBS_ARRAY_INDEX')

# load in input data
lcm = gr.from_file('data/lcm/lcm2007_25m_gb.tif')
# we will need the resolution of the data later when working out the size of the window by number of cells. 
res = lcm.x_cell_size
bng = gpd.read_file('data/bng/10km_grid_region.shp')
#gb = gpd.read_file('data/gb_shapefile/GBR_adm1.shp')
# gb file is in WGS84, needs to be BNG
#gb = gb.to_crs(bng.crs)
pred_id = pd.read_csv('data/worldclim_vars.csv')
pred_id = pred_id.query('JID == ' + str(job_id))

# habitats included in the analysis are 1-11 - these are the habitats mainly 
# used by the farmland indicator bird species - may need to rethink at a later 
# date but seemed reasonable for the time being
lc = np.arange(1, 12)

# we want to loop through the grid cells in this job ID and the three chosen window sizes:
grid_cells = pred_id.grid_ref_levels
# window size for analysis - this is the scale of the process - needs to be in metres
w_sizes = [1000, 1500, 2000]

res = pd.DataFrame()

for grid_ref in grid_cells:
    for w in w_sizes:
        cellb = nlm.get_cell_buffer(bng, grid_ref, w/2)
    
        # clip the environmental data (land cover here) to the buffered cell
        env_clip = lcm.clip(cellb)[0].raster.data
    
        # we're currently avoiding any coastal 10 km cells to avoid edge effects. Here 0 is the no data value
        # any cell with a value of 0 is in the sea.                    
        if (env_clip == 0).sum() == 0:
            # we need a surface of habitat or not (uses in1d to get true/false on elements 
            # of lc and then reshape to convert back to 2d)
            binary = np.reshape(np.in1d(env_clip,lc), (-1, env_clip.shape[0]))
            
            # for each cell, calculate habitat amount within the window
            ls_amount = generic_filter(env_clip, nlm.lc_prop, int(w/res), mode='wrap', extra_keywords = {'lc':lc})*binary
            # for each cell, calculate the habitat heterogeneity within the window
            ls_hetero = generic_filter(env_clip, nlm.shannon, int(w/res), mode='wrap', extra_keywords = {'lc':lc})
            # multiply the amount*hetero*npp
            ls_both = ls_amount * ls_hetero
            out = pd.Series({'grid_ref': grid_ref, 'scale': w, 'ls_amount': np.mean(ls_amount), 'ls_hetero': np.mean(ls_hetero), 'ls_both': np.mean(ls_both)})
            res = res.append(out, ignore_index=True)
            
unique_filename = uuid.uuid4()
res.to_csv('farmland_birds/results/output'+str(unique_filename)+'.csv', index=False)
