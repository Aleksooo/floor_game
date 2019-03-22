import pygame as py
import sys

def button(screen, x_pos, y_pos, index, size = 50):
    level_font = py.font.SysFont('arial', 45).render(str(index), True, (0, 0, 0))
    py.draw.rect(screen, (255, 255, 255), (x_pos, y_pos, size, size))
    screen.blit(level_font, (x_pos + 13, y_pos))

def draw_level_grid(screen, levels_len, levels):

    white = (255, 255, 255)
    black = (0, 0, 0)

    while True:
        py.time.delay(1)
        screen.fill(black)

        len = levels_len
        item_index = 1

        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit(0)

            ''' если в инвенторе есть хоть одна вещ '''
        for y in range(50, 601, 100):
            for x in range(50, 601, 100):
                button(screen, x, y, item_index)
                '''
                if py.mouse.get_pressed()[0] == 1:
                    if py.mouse.get_pos()[0] > x and py.mouse.get_pos()[0] < x + 30 and\
                        py.mouse.get_pos()[1] > y and py.mouse.get_pos()[1] < y + 30:
                        levels = False
                        return levels, item_index - 1
                '''
                for event in py.event.get():
                    if event.type == py.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if py.mouse.get_pos()[0] > x and py.mouse.get_pos()[0] < x + 30 and py.mouse.get_pos()[1] > y and py.mouse.get_pos()[1] < y + 30:
                                levels = False
                                return levels, item_index - 1
                len -= 1
                item_index += 1

                if len == 0:
                    break
            if len == 0:
                break

        py.display.update()