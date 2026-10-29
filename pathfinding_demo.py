import pygame

from modules.binary_space_partitioning import MapGenerator
from modules.pathfinding.node import Node, NodeMap
from modules.pathfinding.a_star import AStar

from modules.registry import Tiles

class Demo:
    def __init__(self):
        pygame.init()
        self.grid_size = 16
        self.grid_dimension = (self.grid_size, self.grid_size)

        self.generator = MapGenerator()
        self.map       = self.generator.generate_map()
        self.pathfinder = AStar(self.map)

        self.screen_width = self.map.width * self.grid_size
        self.screen_height = self.map.height * self.grid_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.clock  = pygame.time.Clock()
        self.fps    = 60

        self.font = pygame.font.Font('assets/CousineNerdFont-Regular.ttf', 15)

        self.start = None
        self.end = None
        self.map_updated = False
        self.path = None

        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.process_event()
            self.process_key()
            self.update()
            self.display()

    def process_event(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 6:
                        pos = self.get_mouse_grid_coordinate()
                        if self.map.is_walkable(pos) and pos != self.start and pos != self.end:
                            self.start = pos
                            self.map_updated = True
                        elif pos == self.start:
                            self.start = None
                            self.map_updated = True

                    if event.button == 7:
                        pos = self.get_mouse_grid_coordinate()
                        if self.map.is_walkable(pos) and pos != self.start and pos != self.end:
                            self.end = pos
                            self.map_updated = True
                        elif pos == self.end:
                            self.end = None
                            self.map_updated = True

    def process_key(self):
        pressed = pygame.mouse.get_pressed(5)
        pos = self.get_mouse_grid_coordinate()

        if pressed[0]:
            if self.map.get(*pos).walkable:
                self.map.set(*pos, Tiles.WALL_TOP)
                self.map_updated = True
        if pressed[2]:
            if not self.map.get(*pos).walkable:
                self.map.set(*pos, Tiles.FLOOR)
                self.map_updated = True

    def update(self):
        if self.map_updated and self.start and self.end:
            self.pathfinder.update_map(self.map)
            self.path = self.pathfinder.pathfind(self.start, self.end)
            print(self.path, end='\n\n')
            self.map_updated = False
        if not self.start or not self.end:
            self.pathfinder.searching = []
            self.pathfinder.processed = []
            self.pathfinder.path = []

    def display(self):
        self.screen.fill('white')
        self.map.display(self.screen, draw_other=True)
        if self.pathfinder:
            self.render_pathfinder(self.screen)

        if self.start:
            pygame.draw.rect(self.screen, 'green', ((self.start[0] * self.grid_size, self.start[1] * self.grid_size), self.grid_dimension))
        if self.end:
            pygame.draw.rect(self.screen, 'red', ((self.end[0] * self.grid_size, self.end[1] * self.grid_size), self.grid_dimension))

        self.draw_grid()
        self.draw_mouse_grid_coordinate(self.screen)
        pygame.display.flip()

    def draw_grid(self):
        for x in range(0, self.screen_width, self.grid_size):
            pygame.draw.line(self.screen, 'black', (x, 0), (x, self.screen_height))

        for y in range(0, self.screen_height, self.grid_size):
            pygame.draw.line(self.screen, 'black', (0, y), (self.screen_width, y))

    def draw_mouse_grid_coordinate(self, surface):
        pos = self.get_mouse_grid_coordinate()
        coordinate_text = self.font.render(f'{str(pos)}, {self.map.is_walkable(pos)}', False, 'black', 'white')

        surface.blit(coordinate_text, (( pos[0] * self.grid_size,
                                        (pos[1] - 1) * self.grid_size)))

    def get_mouse_grid_coordinate(self):
        mouse_pos = pygame.mouse.get_pos()
        return (mouse_pos[0] // self.grid_size, mouse_pos[1] // self.grid_size)

    def render_pathfinder(self, surface):
        for node in self.pathfinder.searching:
            self.draw_node(surface, (34, 200, 34), node)
        for node in self.pathfinder.processed:
            self.draw_node(surface, (0, 128, 128), node)
        for node in self.pathfinder.path:
            self.draw_node(surface, (255, 99, 71), node)

    def draw_node(self, surface, color, node):
            pygame.draw.rect(surface, color, ((node.x * self.grid_size, node.y * self.grid_size), self.grid_dimension))

Demo().run()
pygame.quit()
