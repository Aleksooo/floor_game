from game import *

from levels_class import draw_level_grid

def intro(screen):
    font = py.font.SysFont('arial', 75)
    Dungeon = font.render('Dungeon', True, white)
    trip = font.render('trip', True, white)
    ''' выезжание первого текста '''
    for first_label_x in range(-310, 156, 5):
        screen.fill(black)
        py.time.delay(10)
        screen.blit(Dungeon, (first_label_x, 140))
        py.display.update()
    ''' выезжание второго текста '''
    for first_label_y in range(710, 244, -5):
        screen.fill(black)
        py.time.delay(10)
        screen.blit(Dungeon, (155, 140))
        screen.blit(trip, (first_label_y, 256))
        py.display.update()

def draw_button(x_text_pos, y_text_pos, x_button_pos, y_button_pos, font):
    drawn_rect = (x_button_pos, y_button_pos, 300, 100)
    color = press_button(x_button_pos, y_button_pos, drawn_rect)
    py.draw.rect(screen, color, drawn_rect)
    screen.blit(font, (x_text_pos, y_text_pos))

def press_button(x_button_pos, y_button_pos, drawn_rect):
    global levels, settings
    if py.mouse.get_pos()[0] > x_button_pos and py.mouse.get_pos()[0] < x_button_pos + drawn_rect[2] and py.mouse.get_pos()[1] > y_button_pos and py.mouse.get_pos()[1] < y_button_pos + drawn_rect[3]:

        if py.mouse.get_pressed()[0] == 1:
            if x_button_pos == 150 and y_button_pos == 150:
                levels = True
            elif x_button_pos == 150 and y_button_pos == 320:
                settings = True
            elif x_button_pos == 150 and y_button_pos == 490:
                sys.exit(0)
        return (155, 155, 155)
    else:
        return (255, 255, 255)

width, height = 600, 600
size = 30

black = (0, 0, 0)
white = (255, 255, 255)

py.init()
py.display.set_caption('Dungeon')
screen = py.display.set_mode((width, height))

game = True
person = hero(size, screen, game)

''' проигрывание интро '''
intro(screen)
py.time.delay(2000)
''' переменные для открытия окн '''
levels = False
settings = False
''' шрифты на все случаи жизни '''
Label_font = py.font.SysFont('arial', 60)
Label = Label_font.render('Dungeon trip', True, white)
Level_font = py.font.SysFont('arial', 35)
Level = Level_font.render('Выберите уровень', True, black)
Settings_font = py.font.SysFont('arial', 45)
Setting = Settings_font.render('Настройки', True, black)
Exit_Font = py.font.SysFont('arial', 45)
Exit = Exit_Font.render('Выход', True, black)

while True:
    screen.fill(black)

    for event in py.event.get():
        if event.type == py.QUIT:
            sys.exit(0)

    screen.blit(Label, (140, 20))

    ''' отрисовка кнопки уровней '''
    draw_button(153, 180, 150, 150, Level)
    ''' отрисовка кнопки настроек '''
    draw_button(190, 350, 150, 320, Setting)
    ''' отрисовка кнопки выхода '''
    draw_button(230, 520, 150, 490, Exit)

    if levels:
        levels, person.level_number = draw_level_grid(screen, len(person.all_levels), levels)
        print(person.level_number)
        person.picked_level = person.all_levels[person.level_number]
        person.picked_start_pos = person.level_start_pos[person.level_number]
        person.person_x, person.person_y = person.picked_start_pos
        person.room_number = 0
        main_game(screen, width, height, size, black, white, person, game)
    elif settings:
        pass

    ''' вызов игры '''

    py.display.update()