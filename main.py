import os
import sys

import pygame
import requests

from WINDOW import MyWidget


def repaint_map():
    response = requests.get(map_api_server, params=map_params)
    with open(map_file, "wb") as file:
        file.write(response.content)


map_api_server = "http://static-maps.yandex.ru/1.x/"
map_params = {
    "ll": f'37,57',
    "spn": '0.1,0.1',
    "l": 'map',
    'size': '450,450'
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

running = True
while running:
    ex = MyWidget()
    ex.show()
    print(NAME)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
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
                map_params['spn'] = str(mp) + ',' + str(mp)
            elif keys[pygame.K_PAGEUP]:
                mp = float(map_params["spn"].split(',')[0]) * (1 // shift_scale)
                map_params['spn'] = str(mp) + ',' + str(mp)
            repaint_map()
            screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
