from wikidata.client import Client
import requests
import json

def get_id(query):
    url = "https://www.wikidata.org/w/api.php"

    params = {
        "action": "wbsearchentities",
        "language": "en",
        "format": "json",
        "search": query
    }

    response = requests.get(url, params=params)
    json_data = json.loads(response.text)

    id = json_data["search"][0]["id"]
    return id


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
