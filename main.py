import os
import sys

import pygame
import requests

from addressFind import find_coords_with_address


class LineEdit(pygame.sprite.Sprite):
    def __init__(self):
        super(LineEdit, self).__init__(line_edit_group)
        self.font = pygame.font.SysFont('Comic Sans MS', 20)
        self.text = 'aaa'
        self.image = pygame.surface.Surface((400, 30))
        self.rect = pygame.rect.Rect(10, 10, *self.image.get_size())
        self.text_img = self.font.render(self.text, True, 'black')

    def update(self):
        self.text_img = self.font.render(self.text, True, 'black')
        self.image.fill('white')
        if editing:
            self.image.fill('black')
            self.image.fill('white', (1, 1, self.rect.w - 2, self.rect.h - 2))
        self.image.blit(self.text_img, (10, 0))


def repaint_map():
    response = requests.get(map_api_server, params=map_params)
    with open(map_file, "wb") as file:
        file.write(response.content)


map_api_server = "http://static-maps.yandex.ru/1.x/"
map_params = {
    "ll": f'37,57',
    "spn": '0.1,0.1',
    "l": 'map',
    'size': '450,450',
    'pt': None
}
ls = ['map', 'sat', 'sat,skl']

map_file = "map.png"
repaint_map()

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((450, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()

coords_shift = 0.01
shift_scale = 0.5
NAME = ''

line_edit_group = pygame.sprite.Group()
address_line = LineEdit()

button = pygame.sprite.Sprite(line_edit_group)
button.image = pygame.surface.Surface((30, 30))
button.image.fill('red')
button.rect = pygame.rect.Rect(400, 10, *button.image.get_size())

editing = False
alphabet_corr = 'fа,бdвuгlдtе`ё;жpзbиrкkлvмyнjоgпhрcсnтeуaф[хwцxчiшoщ]ъsыmь\'э.юzя'
alphabet = 'r'

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if not editing:
                if keys[pygame.K_m]:
                    map_params['l'] = ls[ls.index(map_params['l']) - 1]

                if keys[pygame.K_LEFT]:
                    x, y = [float(i) for i in map_params['ll'].split(',')]
                    map_params['ll'] = ','.join((str(x - coords_shift), str(y)))
                elif keys[pygame.K_RIGHT]:
                    x, y = [float(i) for i in map_params['ll'].split(',')]
                    map_params['ll'] = ','.join((str(x + coords_shift), str(y)))
                elif keys[pygame.K_UP]:
                    x, y = [float(i) for i in map_params['ll'].split(',')]
                    map_params['ll'] = ','.join((str(x), str(y + coords_shift)))
                elif keys[pygame.K_DOWN]:
                    x, y = [float(i) for i in map_params['ll'].split(',')]
                    map_params['ll'] = ','.join((str(x), str(y - coords_shift)))

                elif keys[pygame.K_PAGEDOWN]:
                    mp = float(map_params["spn"].split(',')[0]) * shift_scale
                    if mp > 0.006:
                        map_params['spn'] = str(mp) + ',' + str(mp)
                elif keys[pygame.K_PAGEUP]:
                    mp = float(map_params["spn"].split(',')[0]) * (1 // shift_scale)
                    if mp < 100:
                        map_params['spn'] = str(mp) + ',' + str(mp)
                repaint_map()
                screen.blit(pygame.image.load(map_file), (0, 0))
            else:
                key = pygame.key.name(event.key)
                if key == 'left alt':
                    alphabet = 'r' if alphabet == 'a' else 'a'
                if key in alphabet_corr:
                    if alphabet == 'r':
                        address_line.text += alphabet_corr[alphabet_corr.index(key) + 1]
                    else:
                        address_line.text += key
                elif key in '1234567890,.':
                    address_line.text += key
                elif key == 'space':
                    address_line.text += ' '
                elif key == 'backspace':
                    address_line.text = address_line.text[:-1]

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if address_line.rect.collidepoint(*event.pos):
                editing = True
            else:
                editing = False
            if button.rect.collidepoint(*event.pos):
                low_cor, up_cor = find_coords_with_address(address_line.text)['boundedBy']['Envelope'].values()
                coords = find_coords_with_address(address_line.text)['Point']['pos'].split()

                map_params['ll'] = ','.join(coords)
                map_params['pt'] = ','.join((*coords, 'pm2wtm1'))
                print(','.join((*coords, 'pm2wtm1')))
                spn = str(abs(float(low_cor.split()[0]) - float(up_cor.split()[0])))
                map_params['spn'] = ','.join((spn, spn))

                repaint_map()
                screen.blit(pygame.image.load(map_file), (0, 0))

    line_edit_group.update()
    line_edit_group.draw(screen)

    pygame.display.flip()
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
