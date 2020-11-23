from wikidata.client import Client
import requests

def get_id(entity):
    url = "https://www.wikidata.org/w/api.php"

    params = {
        "action": "wbsearchentites"
        "language": "en"
        "format": "json"
        "search": query
    }

    data = requests.get(url, params=params)
    print(type(json))

entity = "alan turing"
get_id(entity)

#
# def get_id(entity):
#
# def get_props(entity):
#
#
# client = Client()
# entity = "Alan Turing"
