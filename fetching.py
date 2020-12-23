import timeit
import requests


def fetch_all(cities):
    responses = []
    with requests.session() as session:
        for city in cities:
            resp = session.get(f"https://geo.api.gouv.fr/communes?nom={city}&fields=nom,region&format=json&geometry=centr")
            responses.append(resp.json())
    return responses