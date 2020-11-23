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
        suggestions = get_suggestions(e)
        output_map[e] = suggestions

    return render_template('output.html',
                            output=request.args.get("output", output),
                            question=request.args.get("question", question))

if __name__ == '__main__':
    app.run()
