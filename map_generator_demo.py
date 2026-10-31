import pygame
import random
from modules.binary_space_partitioning.map import Map

class Demo:
    def __init__(self):
        self.screen_width = 1080
        self.screen_height = 720

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('assets/CousineNerdFont-Regular.ttf', 15)

        self.seed = 'b'
        self.randomizer = random.Random(self.seed)

        self.step = 0
        self.grid_size = 16
        self.room_count = 10
        self.running = True

        self.map = None
        self.map, self.text = self.execute_step(self.map, self.step)

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.process_event()
            self.display()
        pygame.quit()

    def process_event(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False

                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_q:
                            self.running = False
                        case pygame.K_r:
                            self.step_forward()
                            self.map, self.text = self.execute_step(self.map, self.step)
                        case pygame.K_t:
                            while not self.step_forward():
                                self.map, self.text = self.execute_step(self.map, self.step)
                            self.map, self.text = self.execute_step(self.map, self.step)

    def display(self):
        self.screen.fill((25, 25, 25))
        self.map.display(self.screen)
        self.draw_grid(self.grid_size)

        self.screen.blit(self.text, dest=(5, 5))
        self.draw_mouse_grid_coordinate(self.screen)

        pygame.display.flip()

    def step_forward(self):
        self.step += 1
        self.step %= 12
        return self.step == 11

    def execute_step(self, map, step):
        text_color = 'black'
        outline_color = 'white'
        outline_size = 2

        match step:
            case 0:
                map = Map(self.screen_width, self.screen_height, self.randomizer, grid_size=self.grid_size, room_count=self.room_count)
                text = self.render_outlined(self.font, 'Tạo cell root', text_color, outline_color, outline_size)
            case 1:
                map.divide()
                text = self.render_outlined(self.font, f'Chia nhỏ cell root thành các cell con, cho đến khi đạt đủ số lượng yêu cầu ({self.room_count})', text_color, outline_color, outline_size)
            case 2:
                map.get_neighbors()
                text = self.render_outlined(self.font, 'Với mỗi cell, tìm hàng xóm phía bên phải và dưới, hiển thị phải là xanh lá, dưới là xanh lục', text_color, outline_color, outline_size)
            case 3:
                map.shrink()
                text = self.render_outlined(self.font, 'Thu nhỏ kích thước các cell, tạo thành phòng', text_color, outline_color, outline_size)
            case 4:
                map.add_corridors()
                text = self.render_outlined(self.font, 'Thêm đường đi nối giữa các phòng', text_color, outline_color, outline_size)
            case 5:
                map.align()
                text = self.render_outlined(self.font, 'Căn tọa độ các phòng cho trùng với grid tọa độ', text_color, outline_color, outline_size)
            case 6:
                map = map.to_grid()
                text = self.render_outlined(self.font, 'Biến toàn bộ map thành một mảng chứa các phần tử: cell phòng, cell rỗng, cell đường đi', text_color, outline_color, outline_size)
            case 7:
                map.add_spawn_point()
                text = self.render_outlined(self.font, 'Thêm spawn point vào 1 phòng ngẫu nhiên', text_color, outline_color, outline_size)
            case 8:
                map.add_enemies(13)
                text = self.render_outlined(self.font, 'Thêm kẻ địch', text_color, outline_color, outline_size)
            case 9:
                map.fill_wall()
                text = self.render_outlined(self.font, 'Thêm tường bao quanh phòng và hành lang', text_color, outline_color, outline_size)
            case 10:
                map.add_wall_depth()
                text = self.render_outlined(self.font, 'Thay đổi loại tường', text_color, outline_color, outline_size)
            case 11:
                text = self.render_outlined(self.font, 'Xong!', text_color, 'red', outline_size)
        return (map, text)

    def draw_grid(self, grid_size):
        for x in range(self.grid_size, self.screen_width, self.grid_size):
            pygame.draw.rect(self.screen, (25, 25, 25), (x, 0, 1, self.screen_height))

        for y in range(self.grid_size, self.screen_height, self.grid_size):
            pygame.draw.rect(self.screen, (25, 25, 25), (0, y, self.screen_width, 1))

    def get_mouse_grid_coordinate(self):
        mouse_pos = pygame.mouse.get_pos()
        return (mouse_pos[0] // self.grid_size, mouse_pos[1] // self.grid_size)

    def draw_mouse_grid_coordinate(self, surface):
        pos = self.get_mouse_grid_coordinate()
        coordinate_text = self.font.render(str(pos), False, 'black', 'white')
        surface.blit(coordinate_text, (( pos[0] * self.grid_size,
                                        (pos[1] - 1) * self.grid_size)))

    @staticmethod
    def render_outlined(font: pygame.Font,
                        text: str,
                        text_color: pygame.typing.ColorLike,
                        outline_color: pygame.typing.ColorLike,
                        outline_width: int
                       ) -> pygame.Surface:
        old_outline = font.outline
        if old_outline != 0:
            font.outline = 0
        base_text_surf = font.render(text, True, text_color)
        font.outline = outline_width
        outlined_text_surf = font.render(text, True, outline_color)

        outlined_text_surf.blit(base_text_surf, (outline_width, outline_width))
        font.outline = old_outline
        return outlined_text_surf

Demo().run()
