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

    def draw(self):
        start_grid = [(player.camera_y - player.camera_view) / block_size,
                      (player.camera_x - player.camera_view) / block_size]
        stop_grid = [(player.camera_y + player.camera_view) / block_size,
                     (player.camera_x + player.camera_view) / block_size]

        # start_grid[0] -= 1
        # start_grid[1] -= 1
        # stop_grid[0] -= 1
        # stop_grid[1] -= 1

        # print(start_grid, stop_grid)
        for i in range(2):
            if start_grid[i] < 0:
                start_grid[i] -= 1

        int_start_grid = [int(np.floor(start_grid[i])) for i in range(2)]
        int_stop_grid = [int(np.ceil(stop_grid[i])) for i in range(2)]

        # print(int_start_grid, int_stop_grid)

        modulu = [x % 1 for x in start_grid]

        int_x = [int_start_grid[1], int_stop_grid[1]]
        int_y = [int_start_grid[0], int_stop_grid[0]]

        # Stop In Edge Is Hit
        if int_x[0] == 0:
            player.edge_x[0] = True
        else:
            player.edge_x[0] = False

        if int_y[0] == 0:
            player.edge_y[0] = True
        else:
            player.edge_y[0] = False

        if int_y[1] == grid_map.shape[0]:
            player.edge_y[1] = True
        else:
            player.edge_y[1] = False

        if int_x[1] == grid_map.shape[1]:
            player.edge_x[1] = True
        else:
            player.edge_x[1] = False

        # if player.camera_x - player.camera_view < 1:
        #     player.edge_x[0] = True
        # else:
        #     player.edge_x[0] = False
        #
        # if player.camera_y - player.camera_view < 1:
        #     player.edge_y[0] = True
        # else:
        #     player.edge_y[0] = False
        #
        # if player.camera_x + player.camera_view > screen.width:
        #     player.edge_x[1] = True
        # else:
        #     player.edge_x[1] = False
        #
        # if player.camera_y + player.camera_view > screen.height:
        #     player.edge_y[1] = True
        # else:
        #     player.edge_y[1] = False

        for i, x in enumerate(range(*int_x)):
            for j, y in enumerate(range(*int_y)):
                road_num = grid_map[y][x]
                road_x = road_num % 3
                road_y = road_num // 3

                road = roads_img.subsurface(
                    [(roads_img.get_width() / 3) * road_x, (roads_img.get_height() / 4) * road_y,
                     (roads_img.get_width() / 3), roads_img.get_height() / 4])
                screen_block_size_x = self.width / (player.camera_view*2 / block_size)
                screen_block_size_y = self.height / (player.camera_view*2 / block_size)
                road = pygame.transform.scale(road, [screen_block_size_x + 1, screen_block_size_y + 1])
                screen.screen.blit(road, ([(i - modulu[1]) * screen_block_size_x, (j - modulu[0]) * screen_block_size_y]))

        # print(int_x, int_y, start_grid, stop_grid)#player.camera_x, player.camera_y, screen_block_size_x, screen_block_size_y)


class Player:
    def __init__(self):
        self.camera_x = 250
        self.camera_y = 250
        self.camera_view = 150
        self.keys = {'w': 0, 'd': 0, 's': 0, 'a': 0}
        self.edge_x = [False, False]
        self.edge_y = [False, False]

    def keyboard_handler(self):
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

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.keys['w'] = 0
                if event.key == pygame.K_d:
                    self.keys['d'] = 0
                if event.key == pygame.K_s:
                    self.keys['s'] = 0
                if event.key == pygame.K_a:
                    self.keys['a'] = 0

        if self.keys['w']:
            if not self.edge_y[0]:
                self.camera_y -= 1
        if self.keys['d']:
            if not self.edge_x[1]:
                self.camera_x += 1
        if self.keys['s']:
            if not self.edge_y[1]:
                self.camera_y += 1
        if self.keys['a']:
            if not self.edge_x[0]:
                self.camera_x -= 1


screen = Screen()
player = Player()

block_size = 50
# grid_map = np.ones([int(screen.height / block_size), int(screen.width / block_size)], dtype='int')

grid_map = np.array([[1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1],
                     [1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
                     [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1]])

# Game loop.
while True:
    screen.screen.fill((0, 0, 0))

    player.keyboard_handler()

    # Update.
    screen.draw()
    # Draw.

    pygame.display.flip()
    fpsClock.tick(fps)
