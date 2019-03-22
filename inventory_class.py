import pygame as py
import sys

shovel = py.transform.scale(py.image.load('gadgets\\shovel.png'), (100, 100))
bomb = py.transform.scale(py.image.load('gadgets\\bomb.png'), (100, 100))

def draw_inventory(screen, person_inventory):

    white = (255, 255, 255)

    inventory_on = True

    while inventory_on  == True:
        py.time.delay(1)
        screen.fill((144, 144, 144))

        length = len(person_inventory)
        item_index = 0

        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit(0)
            if event.type == py.KEYDOWN:
                if event.key == py.K_e:
                    inventory_on = False
        ''' если в инвенторе ничего нет '''
        if person_inventory == []:
            py.draw.rect(screen, white, (100, 100, 100, 100), 3)
            py.display.flip()
        else:
            ''' если в инвенторе есть хоть одна вещ '''
            for lines in range(1, len(person_inventory) // 4 + 2):
                for places in range(100, 401, 100):
                    if person_inventory[item_index] == '|':
                        screen.blit(shovel, (places, lines * 100, 100, 100))
                        py.draw.rect(screen, white, (places, lines * 100, 100, 100), 3)
                    elif person_inventory[item_index] == '@':
                        screen.blit(bomb, (places, lines * 100, 100, 100))
                        py.draw.rect(screen, white, (places, lines * 100, 100, 100), 3)

                    length -= 1
                    item_index += 1

                    if length == 0:
                        break
                if length == 0:
                    break

            py.display.update()