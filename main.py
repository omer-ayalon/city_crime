import sys
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import numpy as np

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

roads_img = pygame.image.load('assets\\roads1.png')
car_img = pygame.image.load('assets\\car_top2.png')


class Screen:
    def __init__(self):
        self.width, self.height = 600, 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen_block_size_x = self.width / (player.camera_view*2)
        self.screen_block_size_y = self.height / (player.camera_view*2)

    def draw(self):
        self.draw_map()
        self.draw_car()

    def draw_map(self):
        start_grid = [(player.pos[1] - player.camera_view),
                      (player.pos[0] - player.camera_view)]
        stop_grid = [(player.pos[1] + player.camera_view),
                     (player.pos[0] + player.camera_view)]

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
                    screen.screen.blit(road, ([(i - modulu[1]) * self.screen_block_size_x,
                                               (j - modulu[0]) * self.screen_block_size_y]))

    def draw_car(self):
        car = car_img.subsurface(0, 0, car_img.get_width(), car_img.get_height())
        car = pygame.transform.scale(car, [car_img.get_width()/5/player.camera_view,
                                           car_img.get_height()/5/player.camera_view])
        car = pygame.transform.rotate(car, player.ang-90)

        new_rect = car.get_rect(center=(self.width/2, self.height/2))

        screen.screen.blit(car, new_rect)


class Player:
    def __init__(self):
        self.camera_view = 2
        self.pos = [3, 3]
        self.ang = 0
        self.keys = {'w': 0, 'd': 0, 's': 0, 'a': 0, 'q': 0, 'e': 0}

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
                if event.key == pygame.K_e:
                    self.keys['e'] = 1
                if event.key == pygame.K_q:
                    self.keys['q'] = 1

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

    def move(self):
        const_move = 0.05
        const_ang = 3

        if self.keys['w']:
            x = np.sin(np.deg2rad(player.ang)) * const_move
            y = np.cos(np.deg2rad(player.ang)) * const_move
            self.pos[0] += x
            self.pos[1] += y

        if self.keys['s']:
            x = np.sin(np.deg2rad(player.ang)) * const_move
            y = np.cos(np.deg2rad(player.ang)) * const_move
            self.pos[0] -= x
            self.pos[1] -= y

        if self.keys['d']:
            if self.keys['w'] or self.keys['s']:
                player.ang -= const_ang
        if self.keys['a']:
            if self.keys['w'] or self.keys['s']:
                player.ang += const_ang

        # Zoom out
        if self.keys['e']:
            self.camera_view += 0.1
            screen.screen_block_size_x = screen.width / (self.camera_view * 2)
            screen.screen_block_size_y = screen.height / (self.camera_view * 2)

        # Zoom In
        if self.keys['q']:
            if self.camera_view > 1:
                self.camera_view -= 0.1
                screen.screen_block_size_x = screen.width / (self.camera_view * 2)
                screen.screen_block_size_y = screen.height / (self.camera_view * 2)


player = Player()
screen = Screen()

grid_map = np.loadtxt('assets\\map.csv', delimiter=',')

# Game loop.
while True:
    screen.screen.fill((135, 206, 235))

    player.keyboard_handler()

    screen.draw()

    pygame.display.flip()
    fpsClock.tick(fps)
