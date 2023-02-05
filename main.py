import os
import sys

import pygame
import requests

from addressFind import find_coords_with_address


class LineEdit(pygame.sprite.Sprite):
    def __init__(self, x, y, edit_enabled, font_size):
        super(LineEdit, self).__init__(line_edit_group)
        self.edit_enabled = edit_enabled
        self.font = pygame.font.SysFont('Comic Sans MS', font_size)
        self.text = ''
        self.text2 = ''
        self.image = pygame.surface.Surface((400, 30))
        self.rect = pygame.rect.Rect(x, y, *self.image.get_size())

    def update(self):
        self.text_img = self.font.render(self.text, True, 'black')
        self.text_img2 = self.font.render(self.text2, True, 'black')
        self.image.fill('white')
        if editing and self.edit_enabled:
            self.image.fill('black')
            self.image.fill('white', (1, 1, self.rect.w - 2, self.rect.h - 2))
        self.image.blit(self.text_img, (10, 0))
        self.image.blit(self.text_img2, (10, 10))


def repaint_map():
    response = requests.get(map_api_server, params=map_params)
    if response:
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
address_line = LineEdit(10, 10, True, 20)
address_show_line = LineEdit(10, 410, False, 10)

# buttons
if True:
    button = pygame.sprite.Sprite(line_edit_group)
    button.image = pygame.surface.Surface((30, 30))
    button.image.fill('green')
    button.rect = pygame.rect.Rect(400, 10, *button.image.get_size())

    button_reset = pygame.sprite.Sprite(line_edit_group)
    button_reset.image = pygame.surface.Surface((30, 30))
    button_reset.image.fill('red')
    button_reset.rect = pygame.rect.Rect(400, 410, *button_reset.image.get_size())

    button_ind = pygame.sprite.Sprite(line_edit_group)
    button_ind.image = pygame.surface.Surface((30, 30))
    button_ind.image.fill('blue')
    button_ind.rect = pygame.rect.Rect(400, 370, *button_ind.image.get_size())

editing = False
alphabet_corr = 'fа,бdвuгlдtе`ё;жpзbиrкkлvмyнjоgпhрcсnтeуaф[хwцxчiшoщ]ъsыmь\'э.юzя'
alphabet = 'r'

running = True
while running:
    for event in pygame.event.get():
        # pygame quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # KEYBOARD KEY DOWN
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if not editing:
                # NAVIGATING ON MAP IF NOT WRITING LOCATION
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
                # НАЙТИ ВВЕДЕННУЮ ЛОКАЦИЮ
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
            # Если нажали на строку, то можно писать
            if address_line.rect.collidepoint(*event.pos):
                editing = True
            # Если нажали не на строку то прекращаем редактировать
            else:
                editing = False
            # Если нажали на кнопку, то ищем
            if button.rect.collidepoint(*event.pos):
                toponym = find_coords_with_address(address_line.text)
                if toponym is not None:
                    low_cor, up_cor = toponym['boundedBy']['Envelope'].values()
                    coords = find_coords_with_address(address_line.text)['Point']['pos'].split()

                    map_params['ll'] = ','.join(coords)
                    map_params['pt'] = ','.join((*coords, 'pm2wtm1'))
                    spn = str(abs(float(low_cor.split()[0]) - float(up_cor.split()[0])))
                    map_params['spn'] = ','.join((spn, spn))

                    # address show
                    address_label = ' '.join([i['name'] for i in
                                              toponym['metaDataProperty']['GeocoderMetaData']
                                              ['Address']['Components']])

                    address_show_line.text = address_label

                    repaint_map()
                    screen.blit(pygame.image.load(map_file), (0, 0))
            # BUTTON RESET
            if button_reset.rect.collidepoint(*event.pos):
                address_show_line.text = ''
                address_show_line.text2 = ''
                map_params['pt'] = None
                repaint_map()
                screen.blit(pygame.image.load(map_file), (0, 0))
            # BUTTON TO SHOW POSTAL CODE
            if button_ind.rect.collidepoint(*event.pos):
                if not address_show_line.text2 and address_show_line.text:
                    address_show_line.text2 = toponym['metaDataProperty']['GeocoderMetaData']['Address'].get(
                        'postal_code', '')
                elif address_show_line.text:
                    address_show_line.text2 = ''

    line_edit_group.update()
    line_edit_group.draw(screen)

    pygame.display.flip()
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
