import random
from modules.binary_space_partitioning.map import Map

def generate_map(seed=None, grid_size=16, width=70, height=50, room_count=10):
    randomizer = random.Random(seed)
    map = Map(width*grid_size, height*grid_size, randomizer, grid_size=grid_size, room_count=room_count)
    map.divide()
    map.get_neighbors()
    map.shrink()
    map.add_corridors()
    map.add_spawn_point()
    map.align()

    map_grid = map.to_grid()
    map_grid.fill_wall()
    map_grid.add_wall_depth()
    return map_grid
