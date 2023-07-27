import sys
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import numpy as np

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

roads_img = pygame.image.load('assets\\roads1.png')


class Screen:
    def __init__(self):
        self.width, self.height = 600, 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen_block_size_x = self.width / (player.camera_view * 2)
        self.screen_block_size_y = self.height / (player.camera_view * 2)

    def draw(self):
        self.draw_map()

    def draw_map(self):
        start_grid = [(player.camera_y - player.camera_view),
                      (player.camera_x - player.camera_view)]
        stop_grid = [(player.camera_y + player.camera_view),
                     (player.camera_x + player.camera_view)]

        int_start_grid = [int(np.floor(start_grid[i])) for i in range(2)]
        int_stop_grid = [int(np.ceil(stop_grid[i])) for i in range(2)]

        modulu = [x % 1 for x in start_grid]

        int_x = [int_start_grid[1], int_stop_grid[1]]
        int_y = [int_start_grid[0], int_stop_grid[0]]

        # Draw Map
        for i, x in enumerate(range(*int_x)):
            for j, y in enumerate(range(*int_y)):
                if (0 <= y < grid_map.shape[0]) and (0 <= x < grid_map.shape[1]):
                    road_num = grid_map[y][x]
                    road_x = road_num % 3
                    road_y = road_num // 3

                    road = roads_img.subsurface(
                        [(roads_img.get_width() / 3) * road_x, (roads_img.get_height() / 4) * road_y,
                         (roads_img.get_width() / 3), roads_img.get_height() / 4])
                    road = pygame.transform.scale(road, [self.screen_block_size_x + 1, self.screen_block_size_y + 1])
                    screen.screen.blit(road,
                                       ([(i - modulu[1]) * self.screen_block_size_x,
                                         (j - modulu[0]) * self.screen_block_size_y]))


class Player:
    def __init__(self):
        self.camera_x = 5
        self.camera_y = 5
        self.camera_view = 2
        self.keys = {'w': 0, 'd': 0, 's': 0, 'a': 0, 'q': 0, 'e': 0}

    def keyboard_handler(self):
        self.mouse_handle()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_w:
                    self.keys['w'] = 1
                if event.key == pygame.K_d:
                    self.keys['d'] = 1
                if event.key == pygame.K_s:
                    self.keys['s'] = 1
                if event.key == pygame.K_a:
                    self.keys['a'] = 1
                if event.key == pygame.K_e:
                    self.keys['e'] = 1
                if event.key == pygame.K_q:
                    self.keys['q'] = 1
                if event.key == pygame.K_p:
                    np.savetxt('assets\\map.csv', grid_map, delimiter=',')
                    print('Map Saved!')

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.keys['w'] = 0
                if event.key == pygame.K_d:
                    self.keys['d'] = 0
                if event.key == pygame.K_s:
                    self.keys['s'] = 0
                if event.key == pygame.K_a:
                    self.keys['a'] = 0
                if event.key == pygame.K_e:
                    self.keys['e'] = 0
                if event.key == pygame.K_q:
                    self.keys['q'] = 0

        self.move()

    def mouse_handle(self):
        mouse_pos = pygame.mouse.get_pos()
        left, _, right = pygame.mouse.get_pressed()

        start_grid = [player.camera_y - player.camera_view, player.camera_x - player.camera_view]

        x = int((mouse_pos[0] / screen.screen_block_size_x + start_grid[1]) // 1)
        y = int((mouse_pos[1] / screen.screen_block_size_y + start_grid[0]) // 1)

        if left:
            if 0 <= x < grid_map.shape[1] and 0 <= y < grid_map.shape[0]:
                grid_map[y, x] = 0
                refresh_grid()
        if right:
            if 0 <= x < grid_map.shape[1] and 0 <= y < grid_map.shape[0]:
                grid_map[y, x] = 2
                refresh_grid()

    def move(self):
        const = self.camera_view / 20
        if self.keys['w']:
            self.camera_y -= const
        if self.keys['d']:
            self.camera_x += const
        if self.keys['s']:
            self.camera_y += const
        if self.keys['a']:
            self.camera_x -= const

        if self.keys['e']:
            self.camera_view += 0.1
            screen.screen_block_size_x = screen.width / (self.camera_view * 2)
            screen.screen_block_size_y = screen.height / (self.camera_view * 2)

        if self.keys['q']:
            if self.camera_view > 1:
                self.camera_view -= 0.1
                screen.screen_block_size_x = screen.width / (self.camera_view * 2)
                screen.screen_block_size_y = screen.height / (self.camera_view * 2)


def refresh_grid():
    for i in range(grid_map.shape[0]):
        for j in range(grid_map.shape[1]):
            if grid_map[i, j] != 2:
                if i == grid_map.shape[0] - 1 and j == grid_map.shape[1] - 1:
                    mat = {'up': grid_map[i - 1, j], 'down': 2, 'right': 2,
                           'left': grid_map[i, j - 1]}
                elif i == 0 and j == grid_map.shape[1] - 1:
                    mat = {'up': 2, 'down': grid_map[i + 1, j], 'right': 2,
                           'left': grid_map[i, j - 1]}
                elif i == 0:
                    mat = {'up': 2, 'down': grid_map[i + 1, j], 'right': grid_map[i, j + 1],
                           'left': grid_map[i, j - 1]}
                elif j == grid_map.shape[1] - 1:
                    mat = {'up': grid_map[i - 1, j], 'down': grid_map[i + 1, j], 'right': 2,
                           'left': grid_map[i, j - 1]}
                elif j == 0:
                    mat = {'up': grid_map[i - 1, j], 'down': grid_map[i + 1, j], 'right': grid_map[i, j + 1],
                           'left': 2}
                elif i == grid_map.shape[0] - 1:
                    mat = {'up': grid_map[i - 1, j], 'down': 2, 'right': grid_map[i, j + 1],
                           'left': grid_map[i, j - 1]}
                else:
                    mat = {'up': grid_map[i - 1, j], 'down': grid_map[i + 1, j], 'right': grid_map[i, j + 1],
                           'left': grid_map[i, j - 1]}

                if mat['up'] != 2 and mat['down'] != 2 and mat['right'] == 2 and mat['left'] == 2:
                    grid_map[i, j] = 0

                if mat['up'] == 2 and mat['down'] == 2 and mat['right'] != 2 and mat['left'] != 2:
                    grid_map[i, j] = 1

                if mat['up'] == 2 and mat['down'] != 2 and mat['right'] != 2 and mat['left'] == 2:
                    grid_map[i, j] = 3

                if mat['up'] == 2 and mat['down'] != 2 and mat['right'] != 2 and mat['left'] != 2:
                    grid_map[i, j] = 4

                if mat['up'] == 2 and mat['down'] != 2 and mat['right'] == 2 and mat['left'] != 2:
                    grid_map[i, j] = 5

                if mat['up'] != 2 and mat['down'] != 2 and mat['right'] != 2 and mat['left'] == 2:
                    grid_map[i, j] = 6

                if mat['up'] != 2 and mat['down'] != 2 and mat['right'] != 2 and mat['left'] != 2:
                    grid_map[i, j] = 7

                if mat['up'] != 2 and mat['down'] != 2 and mat['right'] == 2 and mat['left'] != 2:
                    grid_map[i, j] = 8

                if mat['up'] != 2 and mat['down'] == 2 and mat['right'] != 2 and mat['left'] == 2:
                    grid_map[i, j] = 9

                if mat['up'] != 2 and mat['down'] == 2 and mat['right'] != 2 and mat['left'] != 2:
                    grid_map[i, j] = 10

                if mat['up'] != 2 and mat['down'] == 2 and mat['right'] == 2 and mat['left'] != 2:
                    grid_map[i, j] = 11


player = Player()
screen = Screen()

# grid_map = np.ones([20, 10], dtype='int') * 2
grid_map = np.loadtxt('assets\\map.csv', delimiter=',')

# Game loop.
while True:
    screen.screen.fill('white')

    player.keyboard_handler()

    screen.draw()

    pygame.display.flip()
    fpsClock.tick(fps)
