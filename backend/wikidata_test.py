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

def get_props(id):
    client = Client()
    entity = client.get(id, load=True)

    occ_prop = str(entity[client.get("P106")])
    occupation_id = occ_prop[occ_prop.find(' ')+1 : occ_prop.find('>')]

    nat_prop = str(entity[client.get("P27")])
    nationality_id = nat_prop[nat_prop.find(' ')+1 : nat_prop.find('>')]

    b_prop = str(entity[client.get("P569")])
    birthday = b_prop[b_prop.find(' ')+1 : b_prop.find('>')]

    props = [occupation_id, nationality_id, birthday_id]

    return props

entity = "alan turing"
id = get_id(entity)

props = get_props(id)
print(props)
#
# def get_id(entity):
#
# def get_props(entity):
#
#
# client = Client()
# entity = "Alan Turing"
