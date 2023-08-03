import json
import sys
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import numpy as np

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

roads_img = pygame.image.load('assets\\textures\\roads1.png')
car_img = pygame.image.load('assets\\textures\\car_top2.png')
building_img = pygame.image.load('assets\\textures\\building.png')
pole_img = pygame.image.load('assets\\textures\\wood_pole.png')


class Screen:
    def __init__(self):
        info = pygame.display.Info()
        self.width, self.height = 800, 600  # info.current_w - 50, info.current_h - 100
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen_block_size_x = self.width / (player.camera_view*2)
        self.screen_block_size_y = self.height / (player.camera_view*2)

    @staticmethod
    def draw_fence():
        pole = pole_img.subsurface(0, 0, pole_img.get_width(), pole_img.get_height())
        pole = pygame.transform.scale(pole, [pole_img.get_width() / player.camera_view * 2,
                                             pole_img.get_height() / player.camera_view * 2])
        start_grid = [(player.pos[1] - player.camera_view),
                      (player.pos[0] - player.camera_view)]
        stop_grid = [(player.pos[1] + player.camera_view),
                     (player.pos[0] + player.camera_view)]

        x_dim = 0.05
        y_dim = 0.1
        y_offset = 0.9
        for i in range(map_dict['road'].shape[0]):
            for j in range(map_dict['road'].shape[1]):
                if (j + 1 - start_grid[1]) > 0 and stop_grid[1] > j and (i + 1 - start_grid[0]) > 0 and stop_grid[0]+0.1 > i:
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

    def draw(self):
        self.draw_map()
        self.draw_car()
        self.draw_fence()

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
                if (0 <= y < map_dict['road'].shape[0]) and (0 <= x < map_dict['road'].shape[1]):
                    road_num = map_dict['road'][y][x]
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

        # self.corners = new_rect.topleft

        screen.screen.blit(car, new_rect)


class Player:
    def __init__(self):
        self.camera_view = 2
        self.pos = [3, 3]
        self.ang = 0
        self.acc = 0.01
        self.speed = 0
        self.max_speed_grass = 0.3
        self.max_speed_road = 0.8
        self.max_speed = self.max_speed_road
        self.keys = {'w': 0, 'd': 0, 's': 0, 'a': 0, 'q': 0, 'e': 0}

    def player_handler(self):
        self.keyboard_handler()
        self.move_car()

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

    def move_car(self):
        w = ((car_img.get_width()/5/self.camera_view)/2) / screen.screen_block_size_x
        h = ((car_img.get_height()/5/self.camera_view)/2) / screen.screen_block_size_y
        for i in range(4):
            if i == 0:
                ww = -w
                hh = -h
                rotate = -1
            elif i == 1:
                ww = w
                hh = -h
                rotate = 1
            elif i == 2:
                ww = -w
                hh = h
                rotate = 1
            else:
                ww = w
                hh = h
                rotate = -1

            c = np.sqrt(ww**2+hh**2)
            ang = np.arctan2(hh, ww) + np.deg2rad(self.ang)

            if map_dict['fence'][int(self.pos[1] // 1) - 1, int(self.pos[0] // 1)][0] == 1:
                if self.pos[1] + np.cos(ang) * c < int(self.pos[1]):
                    self.ang += rotate
                    self.pos[1] = int(self.pos[1]) - np.cos(ang) * c

            if map_dict['fence'][int(self.pos[1] // 1) + 1, int(self.pos[0] // 1)][2] == 1:
                if self.pos[1] + np.cos(ang) * c > int(self.pos[1])+1:
                    self.ang += rotate
                    self.pos[1] = int(self.pos[1])+1 - np.cos(ang) * c

            if map_dict['fence'][int(self.pos[1] // 1), int(self.pos[0] // 1) + 1][1] == 1:
                if self.pos[0] + np.sin(ang) * c > int(self.pos[0]) + 1.05:
                    self.ang += rotate
                    self.pos[0] = int(self.pos[0]) + 1.05 - np.sin(ang) * c

            if map_dict['fence'][int(self.pos[1] // 1), int(self.pos[0] // 1) - 1][3] == 1:
                if self.pos[0] + np.sin(ang) * c < int(self.pos[0]) - 0.05:
                    self.ang += rotate
                    self.pos[0] = int(self.pos[0]) - 0.05 - np.sin(ang) * c

            # if self.pos[0]+np.sin(ang)*c < 0:
            #     self.ang += rotate
            #     self.pos[0] = -np.sin(ang)*c
            #
            # if self.pos[1]+np.cos(ang)*c < 0:
            #     self.ang += rotate
            #     self.pos[1] = -np.cos(ang)*c


        # if self.pos[0] < 0 or self.pos[1] < 0:
        #     self.speed = 0

        # print([player.pos[0]+np.sin(ang)*c,
        #        player.pos[1]+np.cos(ang)*c])

        # pygame.draw.circle(screen.screen, 'green', [(player.pos[0] - start_grid[1])*screen.screen_block_size_x+np.sin(ang)*c,
        #                                             (player.pos[1] - start_grid[0])*screen.screen_block_size_y+np.cos(ang)*c], 5)

        # print((player.pos[0] - start_grid[1])*screen.screen_block_size_x, player.pos[1]*screen.screen_block_size_y)


        # Collision From Borders
        # if self.pos[0]*screen.screen_block_size_x - (car_img.get_width()/5/player.camera_view)/2 < 0:
        #     print('a')
        # car_img.get_height() / 5 / player.camera_view]

        # If Player Drives On Grass, Decrease Speed
        if map_dict['road'][int(self.pos[1]), int(self.pos[0])] == 2:
            self.max_speed = self.max_speed_grass
        else:
            self.max_speed = self.max_speed_road

        # Move Forward
        if self.keys['w']:
            if self.speed < self.max_speed-self.acc:
                self.speed += 2*self.acc
            else:
                self.speed -= self.acc

        # If Nothing Pressed, Bring Speed To 0
        if not self.keys['w'] and not self.keys['s']:
            if -self.acc < self.speed < self.acc:
                self.speed = 0

            if self.speed > 0:
                self.speed -= self.acc
            elif self.speed < 0:
                self.speed += self.acc

        # Move Backwards Or Decrease Speed
        if self.keys['s']:
            if self.speed > -self.max_speed + self.acc:
                self.speed -= 2*self.acc
            else:
                self.speed += self.acc

        # Move Player According To Speed And Angle
        x = np.sin(np.deg2rad(player.ang)) * self.speed/20
        y = np.cos(np.deg2rad(player.ang)) * self.speed/20
        self.pos[0] += x
        self.pos[1] += y

        # Make A Turn; If Speed Is Low, Turning Slower
        const_ang = 3
        if self.keys['d']:
            if self.speed != 0:
                player.ang -= const_ang * np.sqrt(abs(self.speed))
        if self.keys['a']:
            if self.speed != 0:
                player.ang += const_ang * np.sqrt(abs(self.speed))

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

# ==================== Load A Map Or Create A Brand New ==================== #
save_dist = 'assets\\maps\\map2.json'

with open(save_dist, 'r') as infile:
    map_dict = json.load(infile)
map_dict['road'] = np.asarray(map_dict['road'])
map_dict['fence'] = np.asarray(map_dict['fence'])
# ========================================================================== #

# Game loop.
while True:
    screen.screen.fill((135, 206, 235))

    screen.draw()

    player.player_handler()

    pygame.display.flip()
    fpsClock.tick(fps)
    pygame.display.set_caption(str(fpsClock.get_fps()))
