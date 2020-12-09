from flask import Flask, render_template, request
import wikipedia
from nltk.tag import pos_tag
from nltk.tag.stanford import StanfordNERTagger
from wikidata.client import Client
import requests
import json
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)

nltk.download('punkt') # if necessary...
stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


def cosine_sim(text1, text2, vectorizer):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

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

    #print(named_entities[0])
    result = []
    for entity in named_entities_str_tag:
        if(entity[1] == 'PERSON'):
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
    try:
        id = json_data["search"][0]["id"]
        return id
    except:
        return False

def get_props(id):
    client = Client()
    entity = client.get(id, load=True)
    try:
        occ_prop = str(entity[client.get("P106")])
        occupation_id = occ_prop[occ_prop.find(' ')+1 : occ_prop.find('>')]

        nat_prop = str(entity[client.get("P27")])
        nationality_id = nat_prop[nat_prop.find(' ')+1 : nat_prop.find('>')]

        b_prop = str(entity[client.get("P569")])
        birthday = b_prop[b_prop.find(' ')+1 : b_prop.find('>')]

        props = [occupation_id, nationality_id, birthday]

        return props
    except:
        return False

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
    return pd.Series.tolist(results_df["personLabel.value"].tail())

def get_suggestions(entity):
    if(get_id(entity) != False):
        id = get_id(entity)
        if(get_props(id)):
            props = get_props(id)
            return make_sparql_request(id, props)
        else:
            return False
    else:
        return False

def get_wikipedia_paragraph(entity):
    r = requests.get("https://en.wikipedia.org/api/rest_v1/page/summary/" + entity.replace(" ", "_"))
    page = r.json()
    print(page)
    try:
        return page["extract_html"]
    except:
        return page["extract"]

def compute_relevance(main_entity, suggestion):
    vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')
    entity_paragraph = get_wikipedia_paragraph(main_entity)
    try:
        suggestion_paragraph = get_wikipedia_paragraph(suggestion)
        score = cosine_sim(entity_paragraph, suggestion_paragraph, vectorizer)
        return score
    except:
        return 0.0


# Flask Functions Below
@app.route('/')
def hello():
    return render_template('pastIndex.html')

@app.route('/link', methods=['GET','POST'])
def main():
    question = request.form.get("textInput", 0)#Get Input

    output_map = dict()
    output = ""
    links = ""
    entities = link_entities(question)

    entities = list(set(entities))

    for e in entities:
        suggestions = get_suggestions(e) #suggestions is a list
        if(suggestions != False):
            #output_map[e] = suggestions
            for s in suggestions:
                relevance = compute_relevance(e, s)
                output_map[s] = relevance
                links += s + ": " + "https://en.wikipedia.org/wiki/" + s + "\n\n"
            output += "Because you mentioned " + str(e) + " we suggest you talk about: " + str(output_map) + "\n\n"
            output_map = dict()
        # output += (str(output_map) + "\n")

    if(output == ""):
        output = "nothing to suggest!"
    return render_template('output.html',
                            output=request.args.get("output", output),
                            question=request.args.get("question", question),
                            links=request.args.get("links", links),
                            entities=request.args.get("entities", entities))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
