import pygame

from modules.binary_space_partitioning import MapGenerator
from modules.pathfinding.node import Node, NodeMap
from modules.pathfinding.a_star import AStar
from modules.coordinate import Coordinate

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

        self.font = pygame.font.Font('assets/CousineNerdFont-Regular.ttf', 12)

        self.start = None
        self.end = None
        self.map_updated = False
        self.path = None

        self.dt = 0
        self.running = True
        self.full_display = False

        self.shift_x = 0
        self.shift_y = 0
        self.shift_speed = 256

    def run(self):
        while self.running:
            self.dt = self.clock.tick(self.fps) / 1000
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
                    match event.key:
                        case pygame.K_q:
                            self.running = False

                        case pygame.K_f:
                            self.full_display = not self.full_display

                            if self.full_display:
                                self.grid_size = 64
                            else:
                                self.grid_size = 16
                                self.shift_x = 0
                                self.shift_y = 0

                            size = pygame.display.get_desktop_sizes()[0]
                            self.grid_dimension = (self.grid_size, self.grid_size)
                            self.screen_width   = min(size[0], self.map.width * self.grid_size)
                            self.screen_height  = min(size[1], self.map.height * self.grid_size)
                            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
                            pygame.display.set_window_position((0,0))

                        case pygame.K_e:
                            pos = self.get_mouse_grid_coordinate()
                            if self.map.is_walkable(pos) and pos != self.start and pos != self.end:
                                self.start = pos
                                self.map_updated = True
                            elif pos == self.start:
                                self.start = None
                                self.map_updated = True

                        case pygame.K_r:
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
            if self.map.get(pos).walkable:
                self.map.set(pos, Tiles.WALL_TOP)
                self.map_updated = True
        if pressed[2]:
            if not self.map.get(pos).walkable:
                self.map.set(pos, Tiles.FLOOR)
                self.map_updated = True

        if not self.full_display:
            return

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w]:
            self.shift_y += self.shift_speed * self.dt
        if key_pressed[pygame.K_a]:
            self.shift_x += self.shift_speed * self.dt
        if key_pressed[pygame.K_s]:
            self.shift_y -= self.shift_speed * self.dt
        if key_pressed[pygame.K_d]:
            self.shift_x -= self.shift_speed * self.dt

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
        self.screen.fill((25,25,25))
        self.map.display(self.screen, draw_other=True, grid_size=self.grid_size, shift=(self.shift_x, self.shift_y))
        if self.pathfinder:
            self.render_pathfinder(self.screen)

        if self.start:
            pygame.draw.rect(self.screen, (20, 255, 20), ((self.start[0] * self.grid_size + self.shift_x, self.start[1] * self.grid_size + self.shift_y), self.grid_dimension))
        if self.end:
            pygame.draw.rect(self.screen, (128, 0, 0), ((self.end[0] * self.grid_size + self.shift_x, self.end[1] * self.grid_size + self.shift_y), self.grid_dimension))

        self.draw_grid()
        self.draw_mouse_grid_coordinate(self.screen)
        pygame.display.flip()

    def draw_grid(self):
        for x in range(0, self.screen_width, self.grid_size):
            pygame.draw.line(self.screen, 'black', (x + self.shift_x % self.grid_size, 0), (x + self.shift_x % self.grid_size, self.screen_height))

        for y in range(0, self.screen_height, self.grid_size):
            pygame.draw.line(self.screen, 'black', (0, y + self.shift_y % self.grid_size), (self.screen_width, y + self.shift_y % self.grid_size))

    def draw_mouse_grid_coordinate(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        pos = self.get_mouse_grid_coordinate()
        coordinate_text = self.font.render(f'{str(pos)}, {self.map.is_walkable(pos)}', False, 'black', 'white')

        surface.blit(coordinate_text, (mouse_pos[0],
                                       mouse_pos[1] - coordinate_text.size[1]))

    def get_mouse_grid_coordinate(self):
        mouse_pos = pygame.mouse.get_pos()
        return (int(mouse_pos[0] - self.shift_x) // self.grid_size,
                int(mouse_pos[1] - self.shift_y) // self.grid_size)

    def render_pathfinder(self, surface):
        for node in self.pathfinder.searching:
            self.draw_node(surface, (34, 200, 34), node)
        for node in self.pathfinder.processed:
            self.draw_node(surface, (0, 128, 128), node)

        if not self.start or not self.end:
            return

        current = Coordinate.to_coordinate(self.start)
        for relative in self.path:
            current_position = (current * self.grid_size + (self.grid_size // 2) + (self.shift_x, self.shift_y)).tuple()
            target_position =  ((current + relative) * self.grid_size + (self.grid_size // 2) + (self.shift_x, self.shift_y)).tuple()

            pygame.draw.line(surface, 'green', current_position, target_position, 4)
            current = current + relative

    def draw_node(self, surface, color, node):
            padding = 10
            node_x = node.x * self.grid_size + self.shift_x
            node_y = node.y * self.grid_size + self.shift_y
            pygame.draw.rect(surface, color, ((node_x, node_y), self.grid_dimension))
            if self.full_display:
                distance_from_start = self.font.render(str(node.distance_from_start), True, 'black')
                distance_to_end     = self.font.render(str(node.distance_to_end),     True, 'black')
                total_distance      = self.font.render(str(node.total_distance),      True, 'black')

                surface.blit(distance_from_start, (node_x + padding,
                                                   node_y + 0.3 * self.grid_size - 0.5 * distance_from_start.size[1]))
                surface.blit(distance_to_end, (node_x + self.grid_size - distance_to_end.size[0] - padding,
                                               node_y + 0.3 * self.grid_size - 0.5 * distance_to_end.size[1]))
                surface.blit(distance_to_end, (node_x + 0.5 * self.grid_size - 0.5 * distance_to_end.size[0],
                                               node_y + 0.7 * self.grid_size - 0.5 * distance_to_end.size[1]))
Demo().run()
pygame.quit()
