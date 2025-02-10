import os
import sys
import sqlite3
import pygame

pygame.display.init()
size = WIDTH, HEIGHT = 200, 200
screen = pygame.display.set_mode(size)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None, scale=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((5, 5))
            image = pygame.transform.scale(image, (50, 50))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


def terminate():
    pygame.quit()
    sys.exit()


tile_images = {
    'wall': load_image('box.png'),
    'door': load_image('door.jpg', colorkey=-1, scale=True),
    'money': load_image('money.jpg', colorkey=-1, scale=True),
    'ship': load_image('ship.jpg', colorkey=-1, scale=True)
}
player_image = load_image('player.png')
tile_width = tile_height = 50

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        global tile_width
        global tile_height
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    global player_image
    global tile_width
    global tile_height

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos = (pos_x, pos_y)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, x, y):
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)
        self.pos = x, y


class Game:
    def __init__(self, level_number):
        self.levels = ['lvl_1.txt', 'lvl_2.txt', 'lvl_3.txt', 'lvl_4.txt', 'lvl_5.txt']
        self.level_number = level_number
        pygame.init()
        self.FPS = 50
        self.clock = pygame.time.Clock()
        self.size = self.WIDTH, self.HEIGHT = 1300, 700
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill((255, 255, 255))
        self.running = True

        self.fall_delay = 200
        self.fall_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.fall_event, self.fall_delay)
        self.run_delay = 400
        self.run_event = pygame.USEREVENT + 2
        pygame.time.set_timer(self.run_event, self.run_delay)
        self.run_shift_delay = 300
        self.run_shift_event = pygame.USEREVENT + 3
        pygame.time.set_timer(self.run_shift_event, self.run_shift_delay)
        self.second_delay = 1000
        self.second_event = pygame.USEREVENT + 4
        pygame.time.set_timer(self.second_event, self.second_delay)
        self.music1 = pygame.mixer.Sound('music1.mp3')
        self.music2 = pygame.mixer.Sound('music2.mp3')
        self.music3 = pygame.mixer.Sound('music3.mp3')
        self.total = 1
        self.live_time = 0
        self.sky = pygame.image.load('sky.jpg')

    def start_screen(self):

        intro_text = [
            "          Правила игры",
            "Игроку необходимо проходить уровни, преодалевая препятствия",
            "",
            "    Препятствия: ",
            "",
            "Шипы - при попадании на шипы персонаж погибает и игроку",
            "приходится проходить уровень повторно",
            "Дверь - для перехода на следующий уровень, персонажу ",
            "необходимо добраться до двери",
            "",
            "",
            "",
            "",
            "    Управление:",
            "",
            "Движение вперед [D]",
            "Движение назад [A]",
            "Прыжок [SPACE]",
            "Ускорение [Left Shift]"
            "",
            "Для запуска уровня нажмите [Enter]"
        ]

        fon = pygame.transform.scale(load_image('fon3.jpg'), (self.WIDTH, self.HEIGHT))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def nextgame_screen(self):
        intro_text = []

        fon = pygame.transform.scale(load_image('fon2.jpg'), (self.WIDTH, self.HEIGHT))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 50)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)
        self.live_time = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def winner_screen(self):

        intro_text = [f'Вы прошли 5 уровень за {self.live_time} секунд']
        intro_text.append('ВЫ ПРОШЛИ ИГРУ!!!')
        fon = pygame.transform.scale(load_image('fon.jpg'), (self.WIDTH, self.HEIGHT))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def complete_lvl(self):
        intro_text = ['Поздравляем!', f'Вы прошли {self.level_number} уровень за {self.live_time} секунд']
        con = sqlite3.connect("data/records.sqlite")

        # Создание курсора
        cur = con.cursor()
        level_in_english = {
            1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five'
        }
        # Выполнение запроса и получение всех результатов
        result = cur.execute(f"""SELECT {level_in_english[self.level_number]} FROM records""").fetchone()
        con.close()
        print(result)
        if result[0] > self.live_time:
            con = sqlite3.connect("data/records.sqlite")
            cur = con.cursor()
            intro_text.append('У вас новый рекорд')
            cur.execute(f"""UPDATE records
                            SET {level_in_english[self.level_number]} = ?""", (self.live_time, ))
            con.commit()
            con.close()
        fon = pygame.transform.scale(load_image('fon.jpg'), (self.WIDTH, self.HEIGHT))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)
        self.live_time = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def move_map(self, player, movement):
        x, y = player.pos
        if movement == 'up':
            if (self.level[y - 3][x] == '.' or self.level[y - 3][x] == '@' or self.level[y - 3][x] == '&') and \
                    self.level[y + 1][
                        x] == '#' and (
                    self.level[y - 2][x] == '.' or self.level[y - 2][x] == '@' or self.level[y - 2][x] == '&') and (
                    self.level[y - 1][x] == '.' or self.level[y - 1][x] == '@' or self.level[y - 1][x] == '&') and (
                    self.level[y - 4][x] == '.' or self.level[y - 4][x] == '@' or self.level[y - 4][x] == '&'):
                player.move(x, y - 4)
            elif (self.level[y - 3][x] == '.' or self.level[y - 3][x] == '@' or self.level[y - 3][x] == '&') and \
                    self.level[y + 1][
                        x] == '#' and (
                    self.level[y - 2][x] == '.' or self.level[y - 2][x] == '@' or self.level[y - 2][x] == '&') and (
                    self.level[y - 1][x] == '.' or self.level[y - 1][x] == '@' or self.level[y - 1][x] == '&'):
                player.move(x, y - 3)
            elif self.level[y + 1][x] == '#' and (
                    self.level[y - 2][x] == '.' or self.level[y - 2][x] == '@' or self.level[y - 2][x] == '&') and (
                    self.level[y - 1][x] == '.' or self.level[y - 1][x] == '@' or self.level[y - 1][x] == '&') and \
                    self.level[y + 1][
                        x] == '#':
                player.move(x, y - 2)
            elif (self.level[y - 1][x] == '.' or self.level[y - 1][x] == '@' or self.level[y - 1][x] == '&') and \
                    self.level[y + 1][
                        x] == '#':
                player.move(x, y - 1)
        if movement == 'down':
            if self.level[y + 1][x] == '.' or self.level[y + 1][x] == '@' or self.level[y + 1][x] == '&' or \
                    self.level[y + 1][x] == '!':
                if self.level[y + 1][x] == '!':
                    self.music1.stop()
                    self.music2.play()
                    self.total += 1
                    self.nextgame_screen()

                    self.run()
                else:
                    player.move(x, y + 1)
        if movement == 'left':
            if self.level[y][x - 1] == '.' or self.level[y][x - 1] == '@' or self.level[y][x - 1] == '&' or \
                    self.level[y][x - 1] == '!' or self.level[y][x - 1] == '*':
                if self.level[y][x - 1] == '!':
                    self.music1.stop()
                    self.music2.play()
                    self.total += 1
                    self.nextgame_screen()

                    self.run()
                else:
                    player.move(x - 1, y)
        if movement == 'right':
            if self.level[y][x + 1] == '.' or self.level[y][x + 1] == '@' or self.level[y][x + 1] == '&' or \
                    self.level[y][x + 1] == '!' or self.level[y][x - 1] == '*':
                if self.level[y][x + 1] == '!':
                    self.music1.stop()
                    self.music2.play()
                    self.total += 1
                    self.nextgame_screen()

                    self.run()

                else:
                    player.move(x + 1, y)
        if self.level[y][x] == '&':
            self.level_number += 1
            self.complete_lvl()
            self.run()
        if self.level[y][x + 1] == '*':
            self.music1.stop()
            self.music3.play()
            self.winner_screen()

    def generate_level(self, level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if y != 0:
                    if level[y][x] == '#':
                        Tile('wall', x, y)
                        # добавим спрайт в группу
                    elif level[y][x] == '@':
                        new_player = Player(x, y)
                    elif level[y][x] == '&':
                        Tile('door', x, y)
                    elif level[y][x] == '!':
                        Tile('ship', x, y)
                    elif level[y][x] == '*':
                        Tile('money', x, y)
        # вернем игрока, а также размер поля в клетках
        return new_player, x, y

    def run(self):
        self.music2.stop()
        self.music1.stop()
        self.music1.play(-1)
        all_sprites.empty()
        tiles_group.empty()
        player_group.empty()
        self.screen.blit(self.sky, (0, 0))

        self.player = None
        level = self.levels[self.level_number]
        self.level = load_level(level)
        self.player, self.level_x, self.level_y = self.generate_level(self.level)


        while self.running:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == self.second_event:
                    self.live_time += 1
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.fall_event:
                    self.move_map(self.player, 'down')
                if keys[pygame.K_LSHIFT] == 1 and keys[pygame.K_d] == 1 and event.type == self.run_shift_event:
                    self.move_map(self.player, 'right')
                if keys[pygame.K_LSHIFT] == 1 and keys[pygame.K_a] == 1 and event.type == self.run_shift_event:
                    self.move_map(self.player, 'left')
                if keys[pygame.K_d] == 1 and event.type == self.run_event:
                    self.move_map(self.player, 'right')
                if keys[pygame.K_a] == 1 and event.type == self.run_event:
                    self.move_map(self.player, 'left')
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.move_map(self.player, 'up')
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d] == 1:
                self.player.image = load_image('right_mario.png')
            elif keys[pygame.K_a] == 1:
                self.player.image = load_image('left_mario.png')
            else:
                self.player.image = load_image('player.png')
            x, y = self.player.pos
            self.screen.blit(self.sky, (0, 0))
            all_sprites.draw(self.screen)
            player_group.draw(self.screen)
            font = pygame.font.Font(None, 50)
            text = font.render(f'Прошло {self.live_time} секунд', True, (255, 100, 100))
            screen.blit(text, (50, 50))
            pygame.display.flip()
            pygame.display.flip()
            self.clock.tick(50)
        pygame.quit()
