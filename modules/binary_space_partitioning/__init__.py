import random
from modules.binary_space_partitioning.map import Map

class MapGenerator:
    def __init__(self, seed=None, grid_size=16, width=70, height=50, room_count=10):
        self.seed = seed
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.room_count = room_count
        self.randomizer = random.Random(seed)

    def get_state(self):
        return self.randomizer.get_state()

    def set_state(self, state):
        self.randomizer.set_state(state)

    def generate_map(self):
        map = Map(self.width * self.grid_size,
                  self.height * self.grid_size,
                  self.randomizer,
                  grid_size=self.grid_size,
                  room_count=self.room_count)

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
