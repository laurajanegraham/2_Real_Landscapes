# this script holds all the functions for 2_Real_Landscapes.Rmd

# function to process worldclim data to get annual summary for a particular study area
wc_process <- function(dat_folder, crop_shp, proj_shp, fn) {
  out <- list.files(dat_folder, pattern = ".tif", full.names = TRUE) %>%
    lapply(raster) %>%
    stack(.) %>%
    crop(extent(crop_shp)) %>%
    calc(fun = get(fn)) %>%
    projectRaster(crs = proj4string(proj_shp)) %>%
    crop(extent(proj_shp)) %>%
    resample(proj_shp)
} 

# function to scale data between 0 and 1
scale <- function(x) {
  (x-min(x))/(max(x)-min(x))
}

# function to calculate total proportion of included habitat types
lc_prop <- function(values, lc) {
  out = sum(values %in% lc) / length(values)
}

# function to calculate shannon diversity of included habitat types
shannon <- function(values, lc) {
  
  shannon <- 0
  if(sum(values %in% lc) == 0) {
    H = 0  
  } else {
    for(i in lc) {
      p = sum(values %in% i) / sum(values %in% lc)
      if(p == 0) {
        shannon <- shannon + 0
      } else {
        shannon <- shannon + (p * log(p))
      }
    }
    H = -shannon/log(length(lc))
  }
  
  return(H)
}



