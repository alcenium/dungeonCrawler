from modules.world import GridCoordinate

class Camera:
    def __init__(self, screen_width, screen_height, tile_size):
        self.focus     = GridCoordinate(0, 0)
        self.tile_size = tile_size

        self.screen_width  = screen_width
        self.screen_height = screen_height

    def world_to_screen(self, grid_coordinate):
        dx = grid_coordinate.x - self.focus.x 
        dy = grid_coordinate.y - self.focus.y

        return (self.screen_width/2  + dx * self.tile_size,
                self.screen_height/2 + dy * self.tile_size)

    def focus_on(self, grid_coordinate):
        self.focus = grid_coordinate
