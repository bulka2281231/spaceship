import pygame, random, os, sys

#  инициализации pygame
size = width, height = (800, 500)
screen = pygame.display.set_mode(size)
info = pygame.Surface((800, 30))
clock = pygame.time.Clock()
fps = 120


def load_image(name):  # функция принимает файлы
    fullname = os.path.join('', name)
    if not os.path.isfile(fullname):
        print(f"Файл '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Menu:  # класс меню, в котором располагаются две кнопки(play, exit), правила и топ-5
    def __init__(self, button):  # функция получает кнопки
        self.button = button

    def render(self, poverhnost, font, num_punkt):  # функция обратавыет кнопки
        for i in self.button:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self, done=True):
        sets = set()
        file = open('data/Records.txt', mode='r', encoding='utf-8')  # загрузка файла с рекордами
        file_read = file.read().split(':')
        for i in file_read:  # исключение одинаковых рекордов
            if i != '0':
                sets.add(i)
        spis_record = sorted(sets, key=lambda x: int(x))[::-1]  # сортировка рекордов
        print(spis_record)
        if len(file_read) >= 5:
            need_record = spis_record[0:5]
        else:
            need_record = spis_record[0:len(spis_record)]
        font_menu = pygame.font.Font(None, 50)  # создает два размеры текстов
        font_menu_text = pygame.font.Font(None, 30)
        Rules = ['Правила:',
                'Игрок должен управлять своим персонажом,',
                'который бегает по плоскости, ограниченной',
                'стенками. Персонаж может поймать шарик,',
                'один из которых даёт 2 очка и слабо увеличивает',
                'скорость, а другой даёт 10 очков и сильно',
                'увеличивает скорость.',
                'Цель игры: собрать наибольшее количество очков.',
                'Если вы налетите на препятсвие, то персонаж остановится.',
                'Records(Top-5)("Clear"-press space):',
                '1 -',
                '2 -',
                '3 -',
                '4 -',
                '5 -'
                ]
        # координаты расположения строк из списка Rules
        Rules_cord = [45, 65, 85, 105, 125, 145, 165, 185, 205, 245, 265, 285, 305, 325, 345]
        # координаты расположения строк из списка need_record
        Record_cord = [265, 285, 305, 325, 345]
        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        punkt = 0
        while done:
            mp = pygame.mouse.get_pos()
            screen.blit(load_image('data/background.png'), (0, 0))  # загрузка заднего фона меню

            for j in enumerate(Rules_cord):  # выставляем правила
                string = font_menu_text.render(Rules[j[0]], 1, pygame.Color('WHITE'))
                string_rect = string.get_rect()
                string_rect.top = j[1]
                string_rect.x = 200
                screen.blit(string, string_rect)

            for q in enumerate(Record_cord[0:len(need_record)]):  # выставляем рекорды
                string = font_menu_text.render(need_record[q[0]], 1, pygame.Color('WHITE'))
                string_rect = string.get_rect()
                string_rect.top = q[1]
                string_rect.x = 225
                screen.blit(string, string_rect)

            for pos in self.button:  # обрабатывает позиции кнопок
                if (mp[0] > pos[0]) and mp[0] < (pos[0] + 155) and (mp[1] > pos[1]) and mp[1] < pos[1] + 50:
                    punkt = pos[5]
            self.render(screen, font_menu, punkt)

            for e in pygame.event.get():  # при нажатии на определённые кнопки, будут какие-то действия
                if e.type == pygame.QUIT:  # закрытие приложения
                    sys.exit()
                if e.type == pygame.KEYDOWN:  # закрытие приложения
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                if e.type == pygame.KEYDOWN:  # очистка файла
                    if e.key == pygame.K_SPACE:
                        file = open('data/Records.txt', mode='w', encoding='utf-8')
                        file.write('0')
                        file.close()
                        need_record.clear()
                    if e.key == pygame.K_UP:  # выделение кнопки start
                        if punkt > 0:
                            punkt -= 1
                    if e.key == pygame.K_DOWN:  # выделение кнопки exit
                        if punkt < len(self.button) - 1:
                            punkt += 1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 0:
                        done = False
                    elif punkt == 1:
                        exit()

            pygame.display.flip()


class Space_ship(pygame.sprite.Sprite):  # создаем класс персонажа
    image = load_image('data/space_ship.png')
    #  первичное создание персонажа(космического корабля)

    def __init__(self, x, y, screen, vx=1, vy=0):
        super().__init__(all_sprites)
        self.image = Space_ship.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect1x = random.randint(0, 1000)
        self.rect.y = y
        self.rect1y = random.randint(0, 700)
        #  задание скорости движения шарика
        self.vx = vx
        self.vy = vy
        self.screen = screen

    def speed_space_ship_up(self):  # регулирует направление скорости персонажа вверх
        if self.vy > 0:
            pass
        else:
            if self.vx == 0:
                if self.vy > 0:
                    self.vy = -self.vy
            else:
                if self.vx < 0:
                    self.vy = self.vx
                else:
                    self.vy = -self.vx
            self.vx = 0

    def speed_space_ship_down(self):  # регулирует направление скорости персонажа вниз
        if self.vy < 0:
            pass
        else:
            if self.vx == 0:
                if self.vy < 0:
                    self.vy = -self.vy
            else:
                if self.vx < 0:
                    self.vy = -self.vx
                else:
                    self.vy = self.vx
            self.vx = 0

    def speed_space_ship_left(self):  # регулирует направление скорости персонажа влево
        if self.vx > 0:
            pass
        else:
            if self.vy == 0:
                if self.vx < 0:
                    pass
                else:
                    self.vx = -self.vx
            else:
                if self.vy < 0:
                    self.vx = self.vy
                else:
                    self.vx = -self.vy
            self.vy = 0

    def speed_space_ship_right(self):  # регулирует направление скорости персонажа вправо
        if self.vx < 0:
            pass
        else:
            if self.vy == 0:
                if self.vx < 0:
                    self.vx = -self.vx
                else:
                    pass
            else:
                if self.vy < 0:
                    self.vx = -self.vy
                else:
                    self.vx = self.vy
            self.vy = 0

    def speed_change(self):  # увеличение скорости персонаж каждый раз, когда он ловит шарик 5 раз
        global count
        if count % 5 == 0:
            if self.vx > 0:
                self.vx += 1
            if self.vy > 0:
                self.vy += 1
            if self.vx < 0:
                self.vx += -1
            if self.vy < 0:
                self.vy += -1
            count = 0
            print(1)

    def mega_speed_change(self):  # увеличение скорости персонажа в случае, если он поймал супер шарик
        if self.vx > 0:
            self.vx += 1
        if self.vy > 0:
            self.vy += 1
        if self.vx < 0:
            self.vx += -1
        if self.vy < 0:
            self.vy += -1

    def speed_stop(self):  # остановка персонажа
        self.vx = 0
        self.vy = 0

    def coord_change(self):  # удаление(перемещение старого персонажал, если игрок создал нового) персонажа
        self.rect.x = -100
        self.rect.y = -100

    def update(self):
        global score
        #  задание движения шарика
        self.rect = self.rect.move(self.vx, self.vy)
        #  если шарик столкнулся с горизонтальной или вертикальной стеной
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = 0
            GameOver(score)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = 0
            GameOver(score)


#  специализированный класс для задания ограничивающих рамок
class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:         # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class BackGround(pygame.sprite.Sprite):  # класс для создания заднего фона меню
    image = load_image('data/background.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = BackGround.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 30


class NewGame(pygame.sprite.Sprite):  # класс для создания спрайта кнопки 'New game'
    image = load_image('data/new_game.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = NewGame.image
        self.rect = self.image.get_rect()
        self.rect.x = 650
        self.rect.y = 15


class Point(pygame.sprite.Sprite):  # класс для создания спрайта шарика
    image = load_image("data/ball.png")  # загружаем изображение шарика

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Point.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):  # функция отвечает за поведение шариков
        global score
        global flag
        global count
        while True:
            # проверка на коллинеарность шарика с другими спрайтами
            if pygame.sprite.spritecollideany(self, obstacle_borders) or pygame.sprite.collide_circle(self, mega_point):
                self.rect.x = random.randint(50, 750)
                self.rect.y = random.randint(50, 450)
            else:
                break
        # увеличение скорости персонаж каждый раз, когда он ловит шарик 5 раз
        if pygame.sprite.collide_rect(self, space_ship):
            count += 1
            score += 2
            space_ship.speed_change()
            self.rect.x = random.randint(50, 750)
            self.rect.y = random.randint(50, 450)


class Mega_Point(pygame.sprite.Sprite):  # класс для создания спрайта супер шарика
    image = load_image("data/mega_ball.png")  # загружаем изображение супер шарика

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Mega_Point.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):  # функция отвечает за поведение супер шариков
        global score
        global flag
        while True:
            # проверка на коллинеарность шарика с другими спрайтами
            if pygame.sprite.spritecollideany(self, obstacle_borders) or pygame.sprite.collide_circle(self, point):
                self.rect.x = random.randint(50, 750)
                self.rect.y = random.randint(50, 450)
            else:
                break
        # увеличение скорости персонажа в случае, если он поймал супер шарик
        if pygame.sprite.collide_rect(self, space_ship):
            score += 10
            space_ship.mega_speed_change()
            self.rect.x = random.randint(50, 750)
            self.rect.y = random.randint(50, 450)


class Obstacle(pygame.sprite.Sprite):  # класс для создания спрайтов препятсвий
    image = load_image('data/box.png')  # загружаем изображение препятсвий

    def __init__(self, x, y):
        global score
        super().__init__(all_sprites)
        self.image = Obstacle.image
        self.rect = self.image.get_rect()
        self.rect.x = int(x)
        self.rect.y = int(y)
        self.add(obstacle_borders)

    def update(self):  # проверка на коллинеарность шарика с препятсвиями
        global space_ship
        if pygame.sprite.collide_rect(self, space_ship):
            GameOver(score)
            space_ship.speed_stop()  # остановка шариков


def exit_game_to_menu():  # функция дает кнопки с их значениями классу Menu()
    button = [(1, 200, u'Play', (255, 255, 255), (1, 250, 30), 0), (1, 240, u'Exit', (255, 255, 255), (1, 250, 30), 1)]
    game = Menu(button)
    game.menu()


def GameOver(score):  # функция добавляет новый рекорд в файл с рекордами
    file_w = open('data/Records.txt', mode='a', encoding='utf-8')
    if score != 0:
        file_w.write(f':{score}')
    file_w.close()


count = 0  # создаение переменной счётчика
score = 0  # создание переменной очков

# создание групп спрайтов
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
obstacle_borders = pygame.sprite.Group()

# создание шрифтов
pygame.font.init()
score_f = pygame.font.SysFont('Arial', 32)
again = pygame.font.SysFont('Times new roman', 15)

# создает кнопки и передает их значение классу Menu()
button = [(1, 200, u'Play', (255, 255, 255), (1, 250, 30), 0),
            (1, 240, u'Exit', (255, 255, 255), (1, 250, 30), 1)]
game = Menu(button)
game.menu()

#  создание ограничивающих стенок
Border(5, 5, width - 5, 5), Border(5, height - 5, width - 5, height - 5)
Border(5, 5, 5, height - 5), Border(width - 5, 5, width - 5, height - 5)

# создание персонажа
space_ship = Space_ship(200, 90, screen)

# создание обычного шарика
point = Point(random.randint(50, 750), random.randint(50, 450))

# создание супер шарика
mega_point = Mega_Point(random.randint(50, 750), random.randint(50, 450))

# загрузка файлов с координатами нахождения препятсвий
first_level = open('data/Map.txt', mode='r')
data = first_level.read().split(':')
for i in data:
    i = i.replace('(', '').replace(')', '').split(', ')
    Obstacle(i[0], i[1])
    first_level.close()
NewGame()
flag = False


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            space_ship.speed_space_ship_up()  # регулирует направление скорости персонажа вверх
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            space_ship.speed_space_ship_down()  # регулирует направление скорости персонажа вниз
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            space_ship.speed_space_ship_left()  # регулирует направление скорости персонажа влево
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            space_ship.speed_space_ship_right()  # регулирует направление скорости персонажа вправо
        elif event.type == pygame.MOUSEBUTTONDOWN:
            coords = event.pos
            # если игрок кликнул мышкой в област, где находится кнопка 'New game', то начинается новая игра
            if (coords[0] >= 650) and (coords[0] <= 738):
                if (coords[1] >= 15) and (coords[1] <= 34):
                    space_ship.coord_change()  # удаление(перемещение) старого персонажа
                    del_flag = True
                    score = 0  # обновление счёта
                    space_ship = Space_ship(200, 90, screen)  # создание нового персонажа
                    flag = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit_game_to_menu()
    screen.fill((255, 255, 255))  # заполняет экран белым цветом
    screen.blit(score_f.render('Score: ' + str(score), 1, (100, 100, 100)), (350, 0))  # выносит на экран счёт
    for sprite in all_sprites:
        sprite.update()
    for sprite in obstacle_borders:
        sprite.update()
    obstacle_borders.draw(screen)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()