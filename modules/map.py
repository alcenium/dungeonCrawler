class Map:
    def __init__(self, layout, width=0, height=0, types=()):
        self.layout = layout
        self.width  = width
        self.height = height
        self.types = types

    def get_tile(self, x, y):
        return self.types[self.get_type(x, y)]

    def get_type(self, x, y):
        return self.layout[self.get_pos(x, y)]
    
    def get_pos(self, x, y):
        return y * self.width + x
