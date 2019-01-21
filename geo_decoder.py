from yandex_geocoder import Client


def get_coords(address):
    return Client.coordinates(address)
