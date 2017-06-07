library(plyr)

results <- ldply(list.files("farmland_birds/results/", pattern="output", full.names=TRUE), read.csv, stringsAsFactors=FALSE)
coastal <- ldply(list.files("farmland_birds/results/", pattern="coastal", full.names=TRUE), read.csv, stringsAsFactors=FALSE)
cell_list <- read.csv("data/worldclim_vars.csv", stringsAsFactors=FALSE)
cells <- unique(c(results$grid_ref, coastal$grid_ref))

if(setequal(cells, cell_list$grid_ref_levels)) {
	fs <- list.files("farmland_birds/results/", full.names = TRUE)
	file.remove(fs)
	save(results, file="farmland_birds/results/results.rda")
	save(coastal, file="farmland_birds/results/coastal.rda")
} else {
	test <- merge(cell_list, data.frame(grid_ref_levels = cells), all.x = TRUE)
	test <- test[!complete.cases(test),]
	save(test, file="farmland_birds/results/missing_cells.rda")
	print("Not all cells have output - investigate the error files!!")
}
