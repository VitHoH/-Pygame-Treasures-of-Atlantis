import os
import sys

import pygame

pygame.init()
FPS = 50
clock = pygame.time.Clock()
size = WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))


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
    if scale:
        image = pygame.transform.scale(image, (50, 50))
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


start_screen()

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('sky.jpg'),
    'door': load_image('door.jpg'),
    'ship': load_image('ship.png', scale=True)
}
player_image = load_image('player.png')

tile_width = tile_height = 50
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
level = load_level('lvl_1.txt')


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos = (pos_x, pos_y)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, x, y):
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)
        self.pos = x, y


def move_map(player, movement):
    x, y = player.pos
    if movement == 'up':
        if (level[y - 3][x] == '.' or level[y - 3][x] == '@' or level[y - 3][x] == '&') and level[y + 1][x] == '#' and (
                level[y - 2][x] == '.' or level[y - 2][x] == '@' or level[y - 2][x] == '&') and (
                level[y - 1][x] == '.' or level[y - 1][x] == '@' or level[y - 1][x] == '&') and (
                level[y - 4][x] == '.' or level[y - 4][x] == '@' or level[y - 4][x] == '&'):
            player.move(x, y - 4)
        elif (level[y - 3][x] == '.' or level[y - 3][x] == '@' or level[y - 3][x] == '&') and level[y + 1][x] == '#' and (
                level[y - 2][x] == '.' or level[y - 2][x] == '@' or level[y - 2][x] == '&') and (
                level[y - 1][x] == '.' or level[y - 1][x] == '@' or level[y - 1][x] == '&'):
            player.move(x, y - 3)
        elif level[y + 1][x] == '#' and (level[y - 2][x] == '.' or level[y - 2][x] == '@' or level[y - 2][x] == '&') and (
                level[y - 1][x] == '.' or level[y - 1][x] == '@' or level[y - 1][x] == '&') and level[y + 1][x] == '#':
            player.move(x, y - 2)
        elif (level[y - 1][x] == '.' or level[y - 1][x] == '@' or level[y - 1][x] == '&') and level[y + 1][x] == '#':
            player.move(x, y - 1)
    if movement == 'down':
        if level[y + 1][x] == '.' or level[y + 1][x] == '@' or level[y + 1][x] == '&' or level[y + 1][x] == '!':
            if level[y + 1][x] == '!':
                start_screen()
            else:
                player.move(x, y + 1)
    if movement == 'left':
        if level[y][x - 1] == '.' or level[y][x - 1] == '@' or level[y][x - 1] == '&' or level[y][x - 1] == '!':
            if level[y][x - 1] == '!':
                start_screen()
            else:
                player.move(x - 1, y)
    if movement == 'right':
        if level[y][x + 1] == '.' or level[y][x + 1] == '@' or level[y][x + 1] == '&' or level[y][x + 1] == '!':
            if level[y][x + 1] == '!':
                start_screen()
            else:
                player.move(x + 1, y)
    if level[y][x] == '&':
        start_screen()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if y != 0:
                if level[y][x] == '.':
                    Tile('empty', x, y)
                elif level[y][x] == '#':
                    Tile('wall', x, y)
                    # добавим спрайт в группу
                elif level[y][x] == '@':
                    Tile('empty', x, y)
                    new_player = Player(x, y)
                elif level[y][x] == '&':
                    Tile('door', x, y)
                elif level[y][x] == '!':
                    Tile('ship', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


player, level_x, level_y = generate_level(load_level('lvl_1.txt'))
running = True
fall_delay = 200
fall_event = pygame.USEREVENT + 1
pygame.time.set_timer(fall_event, fall_delay)
run_delay = 400
run_event = pygame.USEREVENT + 2
pygame.time.set_timer(run_event, run_delay)
run_shift_delay = 300
run_shift_event = pygame.USEREVENT + 3
pygame.time.set_timer(run_shift_event, run_shift_delay)
while running:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if event.type == fall_event:
            move_map(player, 'down')
        if keys[pygame.K_LSHIFT] == 1 and keys[pygame.K_d] == 1 and event.type == run_shift_event:
            move_map(player, 'right')
        if keys[pygame.K_LSHIFT] == 1 and keys[pygame.K_a] == 1 and event.type == run_shift_event:
            move_map(player, 'left')
        if keys[pygame.K_d] == 1 and event.type == run_event:
            move_map(player, 'right')
        if keys[pygame.K_a] == 1 and event.type == run_event:
            move_map(player, 'left')
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                move_map(player, 'up')
    x, y = player.pos
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(500)
pygame.quit()
