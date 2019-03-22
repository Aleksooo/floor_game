import pygame as py
import time

from Levels.Level1 import Level1_rooms, Level1_start_pos
from Levels.Level2 import Level2_rooms, Level2_start_pos
from Levels.Level3 import Level3_rooms, Level3_start_pos
from Levels.Level4 import Level4_rooms, Level4_start_pos


class hero():

    def __init__(self, size, screen, game):
        ''' переменные о перемещении и отрисовке '''
        self.person_anims = [[py.image.load('hero_texture\\person1R.png'), py.image.load('hero_texture\\person2R.png')],
                             [py.image.load('hero_texture\\person1L.png'), py.image.load('hero_texture\\person2L.png')]]
        self.person = self.person_anims[1][0]
        self.level_start_pos = [Level1_start_pos, Level2_start_pos, Level3_start_pos, Level4_start_pos]
        self.level_number = 0
        self.picked_start_pos = self.level_start_pos[self.level_number]
        self.person_x, self.person_y = self.picked_start_pos
        self.person_x_past, self.person_y_past = self.picked_start_pos
        self.person_rect = py.Rect(self.person_x, self.person_y, size, size)
        ''' переменные о анимации '''
        self.size = size
        self.screen = screen
        self.anim_count = 0
        self.anim_time = 0
        self.turn_side = True
        ''' переменные о переходе в другие комнаты '''
        self.main_room = []
        self.room_number = 0
        self.do_step = True
        ''' все обозначения ловушек '''
        self.catches = ['^', '*']
        ''' вещи в инвенторе '''
        self.in_bag = [] # вещи в инвентрое
        self.packed_items = [] # координаты вещей, которые не надо отрисовывать
        ''' ломание барьера '''
        self.broken_barrier = [] # координаты барьеров, которые сломал игрок
        ''' выбор level '''
        self.all_levels = [Level1_rooms, Level2_rooms, Level3_rooms, Level4_rooms]
        self.picked_level = self.all_levels[self.level_number]
        self.game = game
        ''' звуки '''
        self.shovel_sound = py.mixer.Sound('sounds\\shovel_sound.wav')
        self.bomb_sound = py.mixer.Sound('sounds\\bomb_sound.wav')
        self.win_sound = py.mixer.Sound('sounds\\win_sound.wav')
        self.dead_sound = py.mixer.Sound('sounds\\dead_sound.wav')
        ''' Текст '''
        self.font = py.font.SysFont('arial', 150)
        self.text = self.font.render('Win', True, (255, 255, 255))
    def draw_hero(self, floor_list):
        ''' проверка нахождение в белой зоне '''
        if floor_list[int(self.person_y / self.size)][int(self.person_x / self.size)] != 0:
            ''' проверка на первый шаг при перемещении '''
            if floor_list[int(self.person_y / self.size)][int(self.person_x / self.size)] == 1:
                self.do_step = True
            self.person_x_past = self.person_x
            self.person_y_past = self.person_y
        else:
            self.person_x = self.person_x_past
            self.person_y = self.person_y_past

        self.person_rect = py.Rect(self.person_x, self.person_y, self.size, self.size)
        self.screen.blit(self.person, self.person_rect)

    def play_animation(self):
        ''' проигрывания анимации каждые 400 ms '''
        if self.anim_time < 400:
            self.anim_time += 1
        else:
            self.anim_time = 0

            if self.anim_count < 1:
                self.anim_count += 1
            else:
                self.anim_count = 0

        if self.turn_side:
            self.person = self.person_anims[0][self.anim_count]
        else:
            self.person = self.person_anims[1][self.anim_count]

    def room_change(self, floor_list, width, height):
        y = int(self.person_y / self.size)
        x = int(self.person_x / self.size)

        ''' преход на любой уровень '''
        if str(floor_list[y][x]).isdigit() and self.do_step == True:
            if floor_list[y][x] > 1:

                self.do_step = False
                self.room_number = floor_list[y][x] - 1

                try:
                    if floor_list[y - 1][x] == floor_list[y][x] or floor_list[y + 1][x] == floor_list[y][x]:
                        if self.person_x == 0:
                            self.person_x = width - self.size
                        else:
                            self.person_x = 0
                except IndexError:
                    pass

                try:
                    if floor_list[y][x - 1] == floor_list[y][x] or floor_list[y][x + 1] == floor_list[y][x]:
                        if self.person_y == 0:
                            self.person_y = height - self.size
                        else:
                            self.person_y = 0
                except IndexError:
                    pass

        ''' переход на первый уровень '''
        if floor_list[y][x] == '-' and self.do_step == True:

            self.do_step = False
            self.room_number = 0

            try:
                if floor_list[y - 1][x] == floor_list[y][x] or floor_list[y + 1][x] == floor_list[y][x]:
                    if self.person_x == 0:
                        self.person_x = width - self.size
                    else:
                        self.person_x = 0
            except IndexError:
                pass

            try:
                if floor_list[y][x - 1] == floor_list[y][x] or floor_list[y][x + 1] == floor_list[y][x]:
                    if self.person_y == 0:
                        self.person_y = height - self.size
                    else:
                        self.person_y = 0
            except IndexError:
                pass

    def on_catch(self, floor_list):
        ''' обнулени епосле смерти '''
        if [int(self.person_y / self.size), int(self.person_x / self.size)] not in self.broken_barrier:
            if floor_list[int(self.person_y / self.size)][int(self.person_x / self.size)] in self.catches:
                py.display.update()
                self.dead_sound.play()
                py.time.delay(4000)
                self.person_x = self.picked_start_pos[0]
                self.person_y = self.picked_start_pos[1]
                self.room_number = 0
                self.in_bag = []
                self.packed_items = []
                self.broken_barrier = []

    def add_in_inventory(self, floor_list):
        # если встречается лопата
        if floor_list[int(self.person_y / self.size)][int(self.person_x / self.size)] == '|':
            ''' собирал ли я её раньше '''
            if [int(self.person_y / self.size), int(self.person_x / self.size)] not in self.packed_items:
                self.packed_items += [[int(self.person_y / self.size), int(self.person_x / self.size)]]
                self.in_bag += '|'

        # если встречается бомба
        elif floor_list[int(self.person_y / self.size)][int(self.person_x / self.size)] == '@':
            ''' собирал ли я её раньше '''
            if [int(self.person_y / self.size), int(self.person_x / self.size)] not in self.packed_items:
                self.packed_items += [[int(self.person_y / self.size), int(self.person_x / self.size)]]
                self.in_bag += '@'

    def barrier_break(self, floor_list):
        if self.turn_side: # смотрит направо
            if floor_list[int(self.person_y / self.size)][int(self.person_x / self.size) + 1] == '*':
                if [int(self.person_y / self.size), int(self.person_x / self.size) + 1] not in self.broken_barrier:
                    if '|' in self.in_bag:
                        self.shovel_sound.play()
                        time.sleep(0.4)
                        self.broken_barrier += [[int(self.person_y / self.size), int(self.person_x / self.size) + 1]]
                        self.in_bag.remove('|')
            if floor_list[int(self.person_y / self.size)][int(self.person_x / self.size) + 1] == '^':
                if [int(self.person_y / self.size), int(self.person_x / self.size) + 1] not in self.broken_barrier:
                    if '@' in self.in_bag:
                        self.bomb_sound.play()
                        time.sleep(0.4)
                        self.broken_barrier += [[int(self.person_y / self.size), int(self.person_x / self.size) + 1]]
                        self.in_bag.remove('@')
        else: # смотрит налево
            if floor_list[int(self.person_y / self.size)][int(self.person_x / self.size) - 1] == '*':
                if [int(self.person_y / self.size), int(self.person_x / self.size) + 1] not in self.broken_barrier:
                    if '|' in self.in_bag:
                        self.shovel_sound.play()
                        time.sleep(0.4)
                        self.broken_barrier += [[int(self.person_y / self.size), int(self.person_x / self.size) - 1]]
                        self.in_bag.remove('|')
            if floor_list[int(self.person_y / self.size)][int(self.person_x / self.size) - 1] == '^':
                if [int(self.person_y / self.size), int(self.person_x / self.size) - 1] not in self.broken_barrier:
                    if '@' in self.in_bag:
                        self.bomb_sound.play()
                        time.sleep(0.4)
                        self.broken_barrier += [[int(self.person_y / self.size), int(self.person_x / self.size) - 1]]
                        self.in_bag.remove('@')

    def win(self, floor_list):
        if floor_list[int(self.person_y / self.size)][int(self.person_x / self.size)] == '+':
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.text, (180, 180))
            py.display.update()
            self.win_sound.play()
            py.time.delay(2200)
            return False
        else:
            return True