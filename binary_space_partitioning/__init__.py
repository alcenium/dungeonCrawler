import random
from binary_space_partitioning.map import Map

def generate_map(seed=None, grid_size=16, width=70, height=50, room_count=10):
    randomizer = random.Random(seed)
    map = Map(width*grid_size, height*grid_size, randomizer, grid_size=grid_size, room_count=room_count)
    map.divide()
    map.get_neighbors()
    map.shrink()
    map.add_corridors()
    map.reduce_corridor()
    map.align()
    return map.to_grid()
