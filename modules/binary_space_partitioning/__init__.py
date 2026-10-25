from modules.binary_space_partitioning.map import Map
from random import Random

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any

class MapGenerator:
    def __init__(self, seed: Any = None,
                 grid_size : int = 16,
                 width     : int = 70,
                 height    : int = 50,
                 room_count: int = 10,
                 min_size  : int = 3) -> None:
        self.seed = seed
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.room_count = room_count
        self.min_size = min_size
        self.randomizer: Random = Random(seed)

    def get_state(self):
        return self.randomizer.get_state()

    def set_state(self, state):
        self.randomizer.set_state(state)

    def generate_map(self):
        map = Map(self.width * self.grid_size,
                  self.height * self.grid_size,
                  self.randomizer,
                  grid_size=self.grid_size,
                  room_count=self.room_count,
                  min_size=self.min_size)

        map.divide()
        map.get_neighbors()
        map.shrink()
        map.add_corridors()
        map.align()

        map_grid = map.to_grid()
        map_grid.add_spawn_point()
        map_grid.add_enemies()
        map_grid.fill_wall()
        map_grid.add_wall_depth()
        return map_grid
