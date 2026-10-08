from modules.world import GridCoordinate

class Camera:
    def __init__(self, screen_width, screen_height, tile_size):
        self.focus     = GridCoordinate(0, 0)
        self.tile_size = tile_size

        self.screen_width  = screen_width
        self.screen_height = screen_height

    def grid_to_screen(self, grid_coordinate):
        focus_center_x = self.tile_size / 2
        focus_center_y = self.tile_size / 2

        dx = grid_coordinate.x - self.focus.x 
        dy = grid_coordinate.y - self.focus.y

        return (self.screen_width/2  + dx * self.tile_size - focus_center_x,
                self.screen_height/2 + dy * self.tile_size - focus_center_y)

    def object_visible(self, object):
        x_coordinate = (object.x - self.focus.x) * self.tile_size
        y_coordinate = (object.y - self.focus.y) * self.tile_size

        return (x_coordinate < self.screen_width  - self.tile_size and
                y_coordinate < self.screen_height - self.tile_size)

    def focus_on(self, grid_coordinate):
        self.focus = grid_coordinate
