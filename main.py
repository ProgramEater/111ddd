import os
import sys

import pygame
import requests


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

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((450, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_m]:
                map_params['l'] = ls[ls.index(map_params['l']) - 1]
                repaint_map()
                screen.blit(pygame.image.load(map_file), (0, 0))
            elif keys[pygame.K_PAGEDOWN]:
                mp = float(map_params["spn"].split(',')[0]) * 0.5
                map_params['spn'] = str(mp) + ',' + str(mp)
                repaint_map()
                screen.blit(pygame.image.load(map_file), (0, 0))
            elif keys[pygame.K_PAGEUP]:
                mp = float(map_params["spn"].split(',')[0]) * 2
                map_params['spn'] = str(mp) + ',' + str(mp)
                repaint_map()
                screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
