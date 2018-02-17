# Name: Conway's game of life
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys
import inspect
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# ---

from capyle.ca import Grid2D, Neighbourhood, CAConfig, randomise2d
import capyle.utils as utils
import numpy as np
from random import *


def transition_func(grid, neighbourstates, neighbourcounts, decaygrid_for_chaparral, decaygrid_for_grassland, decaygrid_for_forest):
    # different states that cells can be in
    chaparral, chaparral_burning, grassland, grassland_burning, forest, forest_burning, lake, dead = neighbourcounts

    # probability of fire starting
    percentageChanceOfChaparralIgnite = ((randint(1, 100)) > 91)
    percentageChanceOfGrasslandIgnite = ((randint(1, 100)) > 91)
    percentageChanceOfForestIgnite = ((randint(1, 100)) > 91)

    # if a flammable cell is on fire and it is not a lake then it will ignite with a 10% chance
    birth_of_chaparral_fire = ((chaparral_burning > 0) | (forest_burning > 0) | (grassland_burning > 0)) & (grid == 0) & (grid != 6) & percentageChanceOfChaparralIgnite
    birth_of_grassland_fire = ((chaparral_burning > 0) | (forest_burning > 0) | (grassland_burning > 0)) & (grid == 2) & (grid != 6) & percentageChanceOfGrasslandIgnite
    birth_of_forest_fire = ((chaparral_burning > 0)  | (forest_burning > 0) | (grassland_burning > 0)) & (grid == 4) & (grid != 6) & percentageChanceOfForestIgnite
    
    # as long as there are burning cells the ignited cell will survive
    chaparral_fire_survive = (chaparral_burning > 0) & (grid == 1) & (grid != 6) #& ((randint(1, 10)) > 1)
    grassland_fire_survive = (grassland_burning > 0) & (grid == 1) & (grid != 6) #& ((randint(1, 10)) > 1)
    forest_fire_survive = (forest_burning > 0) & (grid == 1) & (grid != 6) #& ((randint(1, 10)) > 1)

    # set squares on fire
    grid[birth_of_chaparral_fire] = 1
    grid[birth_of_grassland_fire] = 3
    grid[birth_of_forest_fire] = 5



    # setup decay grids for burning tiles to track how long they have been alive
    # when the time limit is reached set them to burnt (dead) tiles
    cells_chaparral_burning = (grid == 1) 
    decaygrid_for_chaparral[cells_chaparral_burning] -= 1
    decayed_to_zero = (decaygrid_for_chaparral == 0)
    grid[decayed_to_zero] = 7

    cells_grassland_burning = (grid == 3) 
    decaygrid_for_grassland[cells_grassland_burning] -= 1
    decayed_to_zero = (decaygrid_for_grassland == 0)
    grid[decayed_to_zero] = 7

    cells_forest_burning = (grid == 5) 
    decaygrid_for_forest[cells_forest_burning] -= 1
    decayed_to_zero = (decaygrid_for_forest == 0)
    grid[decayed_to_zero] = 7


    return grid


def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Conway's game of life"
    config.dimensions = 2
    config.states = (0, 1, 2, 3, 4, 5, 6, 7)
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.state_colors = [(0.749, 0.741, 0.003),(0.921, 0.211, 0.098),(0.498, 0.482, 0.529), (0.984, 0.721, 0.274), (0.309, 0.388, 0.160), (0.733, 0.223, 0.368), (0.223, 0.454, 0.733), (0,0,0)]
    config.num_generations = 2000
    config.grid_dims = (200,200)

    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config


def main():
    # Open the config object
    config = setup(sys.argv[1:])

    # time until the burning square is burnt out
    decaygrid_for_chaparral = np.zeros(config.grid_dims)
    decaygrid_for_chaparral.fill(120)

    decaygrid_for_grassland = np.zeros(config.grid_dims)
    decaygrid_for_grassland.fill(250)

    decaygrid_for_forest = np.zeros(config.grid_dims)
    decaygrid_for_forest.fill(800)


    grid = Grid2D(config, (transition_func, decaygrid_for_chaparral, decaygrid_for_grassland, decaygrid_for_forest))

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
