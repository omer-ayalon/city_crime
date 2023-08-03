"""
Created By - Omer Ayalon

This Is A Code To Design A City And Save It To Play In main.py

Instruction:
A, W, S, D - Move The Camera Around The Map
E, Q - Zoom In And Out

Point The Mouse At A Tile And Left Click To Place A Road
To Delete A Rode Point The Mouse At A Tile And Right Click

P - Save Your City
ESC - Exit The Program
"""

import sys
import numpy as np
from os import environ
import json
from json import JSONEncoder


environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

road_img = pygame.image.load('assets\\textures\\roads1.png')
dirt = pygame.image.load('assets\\textures\\dirt_texture.jpg')
pole_img = pygame.image.load('assets\\textures\\wood_pole.png')


class Screen:
    def __init__(self):
        info = pygame.display.Info()
        self.width, self.height = 800, 600  # info.current_w - 50, info.current_h - 100
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen_block_size_x = self.width / (player.camera_view * 2)
        self.screen_block_size_y = self.height / (player.camera_view * 2)

    def draw(self):
        self.draw_map()
        self.draw_fence()

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
                if (0 <= y < map_dict['road'].shape[0]) and (0 <= x < map_dict['road'].shape[1]):
                    road_num = map_dict['road'][y][x]
                    if road_num == 12:
                        road = dirt.subsurface([0, 0, dirt.get_width(), dirt.get_height()])
                        road = pygame.transform.scale(road,
                                                      [self.screen_block_size_x + 1, self.screen_block_size_y + 1])
                        screen.screen.blit(road,
                                           ([(i - modulu[1]) * self.screen_block_size_x,
                                             (j - modulu[0]) * self.screen_block_size_y]))

                    else:
                        road_x = road_num % 3
                        road_y = road_num // 3

                        road = road_img.subsurface(
                            [(road_img.get_width() / 3) * road_x, (road_img.get_height() / 4) * road_y,
                             (road_img.get_width() / 3), road_img.get_height() / 4])
                        road = pygame.transform.scale(road,
                                                      [self.screen_block_size_x + 1, self.screen_block_size_y + 1])
                        screen.screen.blit(road,
                                           ([(i - modulu[1]) * self.screen_block_size_x,
                                             (j - modulu[0]) * self.screen_block_size_y]))

    def draw_fence(self):
        pole = pole_img.subsurface(0, 0, pole_img.get_width(), pole_img.get_height())
        pole = pygame.transform.scale(pole, [pole_img.get_width() / player.camera_view * 2,
                                             pole_img.get_height() / player.camera_view * 2])
        start_grid = [(player.camera_y - player.camera_view),
                      (player.camera_x - player.camera_view)]
        stop_grid = [(player.camera_y + player.camera_view),
                     (player.camera_x + player.camera_view)]

        x_dim = 0.05
        y_dim = 0.1
        y_offset = 0.9
        for i in range(map_dict['road'].shape[0]):
            for j in range(map_dict['road'].shape[1]):
                if (j + 1 - start_grid[1]) > 0 and stop_grid[1] > j and (i + 1 - start_grid[0]) > 0 and stop_grid[0] > i:
                    if map_dict['fence'][i, j, 0] == 1:
                        for k in range(10):
                            # Row On X Axis Down
                            new_rect = pole.get_rect(
                                center=((j + 1 - x_dim - start_grid[1] - k * 0.1) * screen.screen_block_size_x,
                                        (i + 1 - y_dim - start_grid[0]) * screen.screen_block_size_y))

                            screen.screen.blit(pole, new_rect)

                    if map_dict['fence'][i, j, 1] == 1:
                        for k in range(5):
                            # Row On y Axis Left
                            new_rect = pole.get_rect(
                                center=((j + 1 - x_dim - start_grid[1] - 0.9) * screen.screen_block_size_x,
                                        (i + 1 - y_dim - start_grid[0] - k * 0.227) * screen.screen_block_size_y))

                            screen.screen.blit(pole, new_rect)

                    if map_dict['fence'][i, j, 2] == 1:
                        for k in range(10):
                            # Row On X Axis Up
                            new_rect = pole.get_rect(
                                center=((j + 1 - x_dim - start_grid[1] - k * 0.1) * screen.screen_block_size_x,
                                        (i + 1 - y_dim - start_grid[0] - y_offset) * screen.screen_block_size_y))

                            screen.screen.blit(pole, new_rect)

                    if map_dict['fence'][i, j, 3] == 1:
                        for k in range(5):
                            # Row On y Axis Right
                            new_rect = pole.get_rect(
                                center=((j + 1 - x_dim - start_grid[1]) * screen.screen_block_size_x,
                                        (i + 1 - y_dim - start_grid[0] - k * 0.227) * screen.screen_block_size_y))

                            screen.screen.blit(pole, new_rect)


# Used To Save Properly Numpy Array To JSON File
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


class Player:
    def __init__(self):
        self.camera_x = 5
        self.camera_y = 5
        self.camera_view = 2
        self.keys = {'w': 0, 'd': 0, 's': 0, 'a': 0, 'q': 0, 'e': 0}
        self.select_type = 'r'

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
                if event.key == pygame.K_r:
                    self.select_type = 'r'
                if event.key == pygame.K_f:
                    self.select_type = 'f'
                if event.key == pygame.K_p:
                    with open(save_dist, 'w') as outfile:
                        json.dump(map_dict, outfile, cls=NumpyArrayEncoder)
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
            if 0 <= x < map_dict['road'].shape[1] and 0 <= y < map_dict['road'].shape[0]:
                if player.select_type == 'r':
                    map_dict['road'][y, x] = 0
                elif player.select_type == 'f':
                    map_dict['fence'][y, x] = 1
                refresh_grid()
        if right:
            if 0 <= x < map_dict['road'].shape[1] and 0 <= y < map_dict['road'].shape[0]:
                if player.select_type == 'r':
                    map_dict['road'][y, x] = 2
                elif player.select_type == 'f':
                    map_dict['fence'][y, x] = 0
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
    for i in range(map_dict['road'].shape[0]):
        for j in range(map_dict['road'].shape[1]):
            if player.select_type == 'r':
                if map_dict['road'][i, j] != 2:
                    if i == map_dict['road'].shape[0] - 1 and j == map_dict['road'].shape[1] - 1:
                        mat = {'up': map_dict['road'][i - 1, j], 'down': 2, 'right': 2,
                               'left': map_dict['road'][i, j - 1]}
                    elif i == 0 and j == map_dict['road'].shape[1] - 1:
                        mat = {'up': 2, 'down': map_dict['road'][i + 1, j], 'right': 2,
                               'left': map_dict['road'][i, j - 1]}
                    elif i == 0:
                        mat = {'up': 2, 'down': map_dict['road'][i + 1, j], 'right': map_dict['road'][i, j + 1],
                               'left': map_dict['road'][i, j - 1]}
                    elif j == map_dict['road'].shape[1] - 1:
                        mat = {'up': map_dict['road'][i - 1, j], 'down': map_dict['road'][i + 1, j], 'right': 2,
                               'left': map_dict['road'][i, j - 1]}
                    elif j == 0:
                        mat = {'up': map_dict['road'][i - 1, j], 'down': map_dict['road'][i + 1, j],
                               'right': map_dict['road'][i, j + 1],
                               'left': 2}
                    elif i == map_dict['road'].shape[0] - 1:
                        mat = {'up': map_dict['road'][i - 1, j], 'down': 2, 'right': map_dict['road'][i, j + 1],
                               'left': map_dict['road'][i, j - 1]}
                    else:
                        mat = {'up': map_dict['road'][i - 1, j], 'down': map_dict['road'][i + 1, j],
                               'right': map_dict['road'][i, j + 1],
                               'left': map_dict['road'][i, j - 1]}

                    if mat['up'] != 2 and mat['down'] != 2 and mat['right'] == 2 and mat['left'] == 2:
                        map_dict['road'][i, j] = 0

                    if mat['up'] == 2 and mat['down'] == 2 and mat['right'] != 2 and mat['left'] != 2:
                        map_dict['road'][i, j] = 1

                    if mat['up'] == 2 and mat['down'] != 2 and mat['right'] != 2 and mat['left'] == 2:
                        map_dict['road'][i, j] = 3

                    if mat['up'] == 2 and mat['down'] != 2 and mat['right'] != 2 and mat['left'] != 2:
                        map_dict['road'][i, j] = 4

                    if mat['up'] == 2 and mat['down'] != 2 and mat['right'] == 2 and mat['left'] != 2:
                        map_dict['road'][i, j] = 5

                    if mat['up'] != 2 and mat['down'] != 2 and mat['right'] != 2 and mat['left'] == 2:
                        map_dict['road'][i, j] = 6

                    if mat['up'] != 2 and mat['down'] != 2 and mat['right'] != 2 and mat['left'] != 2:
                        map_dict['road'][i, j] = 7

                    if mat['up'] != 2 and mat['down'] != 2 and mat['right'] == 2 and mat['left'] != 2:
                        map_dict['road'][i, j] = 8

                    if mat['up'] != 2 and mat['down'] == 2 and mat['right'] != 2 and mat['left'] == 2:
                        map_dict['road'][i, j] = 9

                    if mat['up'] != 2 and mat['down'] == 2 and mat['right'] != 2 and mat['left'] != 2:
                        map_dict['road'][i, j] = 10

                    if mat['up'] != 2 and mat['down'] == 2 and mat['right'] == 2 and mat['left'] != 2:
                        map_dict['road'][i, j] = 11

            if player.select_type == 'f':
                if j == 0:
                    map_dict['fence'][i][0][1] = 1
                    map_dict['fence'][i][map_dict['fence'].shape[1] - 1][3] = 1
                if i == 0:
                    map_dict['fence'][0][j][2] = 1
                    map_dict['fence'][map_dict['fence'].shape[0] - 1][j][0] = 1

                if any(map_dict['fence'][i, j]):
                    map_dict['fence'][i, j] = 0
                    if i != map_dict['fence'].shape[0] - 1:
                        if not any(map_dict['fence'][i + 1, j]):
                            map_dict['fence'][i, j, 0] = 1
                    else:
                        map_dict['fence'][i, j, 0] = 1

                    if j > 0:
                        if not any(map_dict['fence'][i, j - 1]):
                            map_dict['fence'][i, j, 1] = 1
                    else:
                        map_dict['fence'][i, j, 1] = 1

                    if i > 0:
                        if not any(map_dict['fence'][i - 1, j]):
                            map_dict['fence'][i, j, 2] = 1
                    else:
                        map_dict['fence'][i, j, 2] = 1

                    if j != map_dict['fence'].shape[1] - 1:
                        if not any(map_dict['fence'][i, j + 1]):
                            map_dict['fence'][i, j, 3] = 1
                    else:
                        map_dict['fence'][i, j, 3] = 1

                    if j > 0 and i > 0 and i != map_dict['fence'].shape[0] - 1 and j != map_dict['fence'].shape[1] - 1:
                        if any(map_dict['fence'][i - 1, j]) and any(map_dict['fence'][i, j + 1]) and \
                                any(map_dict['fence'][i + 1, j]) and any(map_dict['fence'][i, j - 1]):
                            map_dict['fence'][i, j] = 4


def add_boundaries():
    for i in range(map_dict['road'].shape[0]):
        for j in range(map_dict['road'].shape[1]):
            if j == 0:
                map_dict['fence'][i][0][1] = 1
                map_dict['fence'][i][map_dict['fence'].shape[1] - 1][3] = 1
            if i == 0:
                map_dict['fence'][0][j][2] = 1
                map_dict['fence'][map_dict['fence'].shape[0] - 1][j][0] = 1


player = Player()
screen = Screen()

# ==================== Load A Map Or Create A Brand New ==================== #
save_dist = 'assets\\maps\\map2.json'
take_dist = 'assets\\maps\\map1.json'

with open(take_dist, 'r') as infile:
    map_dict = json.load(infile)
map_dict['road'] = np.asarray(map_dict['road'])
map_dict['fence'] = np.asarray(map_dict['fence'])
# ========================================================================== #

# Game loop.
while True:
    screen.screen.fill('white')

    screen.draw()
    player.keyboard_handler()

    pygame.display.flip()
    fpsClock.tick(fps)
    pygame.display.set_caption(str(fpsClock.get_fps()))
