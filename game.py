import pygame as py
import sys

from person_class import hero
from inventory_class import draw_inventory

def main_game(screen , width, height, size, black, white, person, game):

    def draw_floor(floor_list):
        global game
        x_pos, y_pos = 0, 0
        for y in range(len(floor_list)):
            for x in range(len(floor_list[y])):
                ''' отрисовка заднего фона '''
                if floor_list[y][x] == 0:
                    py.draw.rect(screen, black, (x_pos, y_pos, size, size))
                elif floor_list[y][x] != 0:
                    # отрисовка шипов
                    if floor_list[y][x] == '^':
                        if [y, x] not in person.broken_barrier:
                            screen.blit(py.image.load('catches\\pin.png'), (int(x * size), int(y * size), size, size))
                    # отрисовка кустов
                    elif floor_list[y][x] == '*':
                        if [y, x] not in person.broken_barrier:
                            screen.blit(py.image.load('catches\\bush.png'), (int(x * size), int(y * size), size, size))
                    # отрисовка лопаты
                    elif floor_list[y][x] == '|':
                        if [y, x] not in person.packed_items:
                            screen.blit(py.image.load('gadgets\\shovel.png'), (int(x * size), int(y * size), size, size))
                    # отрисовка бомбы
                    elif  floor_list[y][x] == '@':
                        if [y, x] not in person.packed_items:
                            screen.blit(py.image.load('gadgets\\bomb.png'), (int(x * size), int(y * size), size, size))
                x_pos += size
            x_pos = 0
            y_pos += size

    run = False

    while game == True:
        py.time.delay(1)
        screen.fill(white)
        '''
        if privious_level != person.level_number:
            person = hero(size, screen, game)
        '''
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit(0)
            elif event.type == py.KEYDOWN:
                if run == False:
                    if event.key == py.K_RIGHT:
                        if person.person_x < width - size:
                            person.person_x += size
                            person.turn_side = True
                            run = True
                    elif event.key == py.K_LEFT:
                        if person.person_x > 0:
                            person.person_x -= size
                            person.turn_side = False
                            run = True
                    elif event.key == py.K_UP:
                        if person.person_y > 0:
                            person.person_y -= size
                            run = True
                    elif event.key == py.K_DOWN:
                        if person.person_y < height - size:
                            person.person_y += size
                            run = True
                if event.key == py.K_e:
                    draw_inventory(screen, person.in_bag)
                if event.key == py.K_SPACE:
                    person.barrier_break(person.picked_level[person.room_number]) # ломание припятствия


        keys = py.key.get_pressed()
        if run == True:
            py.time.delay(50)
            if keys[py.K_RIGHT]:
                py.time.delay(50)
                if person.person_x < width - size:
                    person.person_x += size
                    person.turn_side = True
            elif keys[py.K_LEFT]:
                py.time.delay(50)
                if person.person_x > 0:
                    person.person_x -= size
                    person.turn_side = False
            elif keys[py.K_UP]:
                py.time.delay(50)
                if person.person_y > 0:
                    person.person_y -= size
            elif keys[py.K_DOWN]:
                py.time.delay(50)
                if person.person_y < height - size:
                    person.person_y += size
            elif keys == []:
                run = False

        draw_floor(person.picked_level[person.room_number]) # отрисовка заднего фона
        person.play_animation() #  изменение анимации
        person.draw_hero(person.picked_level[person.room_number]) # отрисовка персонажа
        person.on_catch(person.picked_level[person.room_number]) # проверка на попадание в ловушку
        person.add_in_inventory(person.picked_level[person.room_number]) # добавление в инвентарь
        person.room_change(person.picked_level[person.room_number], width, height) # проверка на переход
        game = person.win(person.picked_level[person.room_number])

        py.display.update()