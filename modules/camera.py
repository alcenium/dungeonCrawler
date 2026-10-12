from modules.world import GridCoordinate

class Camera:
    def __init__(self, screen_width: int, screen_height: int, tile_size: int) -> None:
        self.focus     = GridCoordinate(0, 0)
        self.tile_size = tile_size

        self.screen_width  = screen_width
        self.screen_height = screen_height

    def grid_to_screen(self, grid_coordinate: GridCoordinate) -> tuple[int, int]:
        """ Chuyển đổi từ tọa độ grid sang tọa độ trên màn hình """
        focus_center_x: int = self.tile_size // 2
        focus_center_y: int = self.tile_size // 2

        dx: int = grid_coordinate.x - self.focus.x 
        dy: int = grid_coordinate.y - self.focus.y

        return (self.screen_width //2 + dx * self.tile_size - focus_center_x,
                self.screen_height//2 + dy * self.tile_size - focus_center_y)

    def object_visible(self, object: GridCoordinate) -> bool:
        """ Vật thể có trên màn hình hay không """
        x_coordinate: int = (object.x - self.focus.x) * self.tile_size
        y_coordinate: int = (object.y - self.focus.y) * self.tile_size

        return (x_coordinate < self.screen_width  - self.tile_size and
                y_coordinate < self.screen_height - self.tile_size)

    def focus_on(self, grid_coordinate) -> None:
        """ Chọn tọa độ trung tâm của màn hình """
        self.focus = grid_coordinate
