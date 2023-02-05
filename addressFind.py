import requests


def find_coords_with_address(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geo_params = {
        'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
        'geocode': address,
        'format': 'json'
    }

    # Выполняем запрос.
    response = requests.get(geocoder_api_server, params=geo_params)
    return response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]