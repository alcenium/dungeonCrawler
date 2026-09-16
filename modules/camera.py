class Camera:
    def __init__(self, screen_width, screen_height):
        self.focus = None
        self.screen_width = screen_width
        self.screen_height = screen_height

    def world_to_screen(self, world_coord):
        if self.focus == None:
            return (self.screen_width//2 + world_coord[0],
                    self.screen_height//2 + world_coord[1])
        else:
            return (self.screen_width//2 + world_coord[0] - self.focus[0],
                    self.screen_height//2 + world_coord[1] - self.focus[1])

    def focus_on(self, world_coord):
        self.focus = world_coord

