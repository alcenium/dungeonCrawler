import pygame
import random
from modules.binary_space_partitioning.map import Map

screen_width = 1080
screen_height = 720

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
font = pygame.font.Font('assets/CousineNerdFont-Regular.ttf', 12)

seed = 'b'
randomizer = random.Random(seed)

step = 0
grid_size = 16
room_count = 10
running = True

def execute_step(map, step):
    match step:
        case 0:
            map = Map(screen_width, screen_height, randomizer, grid_size=grid_size, room_count=room_count)
            text = font.render('Tạo cell root', False, 'white')
        case 1:
            map.divide()
            text = font.render(f'Chia nhỏ cell root thành các cell con, cho đến khi đạt đủ số lượng yêu cầu ({room_count})', False, 'white')
        case 2:
            map.get_neighbors()
            text = font.render('Với mỗi cell, tìm hàng xóm phía bên phải và dưới, hiển thị phải là xanh lá, dưới là xanh lục', False, 'white')
        case 3:
            map.shrink()
            text = font.render('Thu nhỏ kích thước các cell, tạo thành phòng', False, 'white')
        case 4:
            map.add_corridors()
            text = font.render('Thêm đường đi nối giữa các phòng', False, 'white')
        case 5:
            map.add_spawn_point()
            text = font.render('Thêm spawn point vào 1 phòng ngẫu nhiên', False, 'white')
        case 6:
            map.add_enemies()
            text = font.render('Thêm kẻ địch', False, 'white')
        case 7:
            map.align()
            text = font.render('Căn tọa độ các phòng cho trùng với grid tọa độ', False, 'white')
        case 8:
            map = map.to_grid()
            text = font.render('Biến toàn bộ map thành một mảng chứa các phần tử: cell phòng, cell rỗng, cell đường đi', False, 'white')
        case 9:
            map.fill_wall()
            text = font.render('Thêm tường bao quanh phòng và hành lang', False, 'white')
        case 10:
            map.add_wall_depth()
            text = font.render('Thay đổi loại tường', False, 'white')

    return (map, text)

def draw_grid(grid_size):
    for x in range(grid_size, screen_width, grid_size):
        pygame.draw.rect(screen, (25, 25, 25), (x, 0, 1, screen_height))

    for y in range(grid_size, screen_height, grid_size):
        pygame.draw.rect(screen, (25, 25, 25), (0, y, screen_width, 1))

map = None
map, text = execute_step(map, step)

while running:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False

            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q:
                        running = False
                    case pygame.K_r:
                        step += 1
                        step %= 11
                        map, text = execute_step(map, step)

    screen.fill((25, 25, 25))
    map.display(screen)
    draw_grid(grid_size)

    screen.blit(text, dest=(5, 5))

    pygame.display.flip()

    clock.tick(60)
