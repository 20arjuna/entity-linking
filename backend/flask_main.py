from flask import Flask, render_template, request
import wikipedia
import tagme
from nltk.tag import pos_tag
from nltk.tag.stanford import StanfordNERTagger

app = Flask(__name__)

def get_continuous_chunks(tagged_sent):
    continuous_chunk = []
    current_chunk = []

    for token, tag in tagged_sent:
        if tag != "O":
            current_chunk.append((token, tag))
        else:
            if current_chunk: # if the current chunk is not empty
                continuous_chunk.append(current_chunk)
                current_chunk = []
    # Flush the final current_chunk into the continuous_chunk, if any.
    if current_chunk:
        continuous_chunk.append(current_chunk)
    return continuous_chunk


def link_entities(question):
    st = StanfordNERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')
    tagged_sent = st.tag(question.split())
    named_entities = get_continuous_chunks(tagged_sent)
    named_entities_str_tag = [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities]

    print(named_entities[0])
    result = []
    for entity in named_entities_str_tag:
        if(entity[1] == 'PERSON'):
            print("yup")
            result.append(entity[0])

    return result

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


            filter (?birth > """ + '"' + propList[2] + '"' + """^^xsd:dateTime)

            SERVICE wikibase:label {
                bd:serviceParam wikibase:language "en" .
            }
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    results_df = pd.io.json.json_normalize(results['results']['bindings'])
    return pd.Series.tolist(results_df["personLabel.value"].head())

def get_suggestions(entity):
    id = get_id(entity)
    props = get_props(id)
    return make_sparql_request(id, props)


# Flask Functions Below
@app.route('/')
def hello():
    return render_template('pastIndex.html')

@app.route('/link', methods=['GET','POST'])
def main():
    question = request.form.get("textInput", 0)#Get Input

    output_map = dict()
    entities = link_entities(question)

    for e in entities:
        suggestions = get_suggestions(e) #suggestions is a list
        output_map[e] = suggestions

    print output_map

    return render_template('output.html',
                            output=request.args.get("output", output),
                            question=request.args.get("question", question))

if __name__ == '__main__':
    app.run()
