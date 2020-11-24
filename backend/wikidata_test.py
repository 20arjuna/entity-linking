from wikidata.client import Client
import requests
import json
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd


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

    props = [occupation_id, nationality_id, birthday]

    return props

def make_sparql_request(entity_id, propList):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    sparql.setQuery(
        """SELECT ?person ?personLabel

        WHERE
        {
            ?person wdt:P21 wd:Q6581072 .
            ?person wdt:P106 wd:""" + propList[0] + """ .
            ?person wdt:P569 ?birth .
            ?person wdt:P27 wd:""" + propList[1] + """ .


            filter (?birth > """ + propList[2] + """^^xsd:dateTime)

            SERVICE wikibase:label {
                bd:serviceParam wikibase:language "en" .
            }
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    results_df = pd.io.json.json_normalize(results['results']['bindings'])
    print(results_df[['item.value', 'itemLabel.value']].head())


entity = "alan turing"
id = get_id(entity)

props = get_props(id)
make_sparql_request(id, props)
#
# def get_id(entity):
#
# def get_props(entity):
#
#
# client = Client()
# entity = "Alan Turing"
