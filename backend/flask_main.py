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
    tagged_sent = pos_tag(question.split())
    entities = [word for word,pos in tagged_sent if pos == 'NNP']
    return entities




# Flask Functions Below
@app.route('/')
def hello():
    return render_template('pastIndex.html')

@app.route('/link', methods=['GET','POST'])
def main():
    question = request.form.get("textInput", 0)
    output = str(link_entities(question)) #Get Input



    stner = StanfordNERTagger()
    tagged_sent = stner.tag(question.split())
    named_entities = get_continuous_chunks(tagged_sent)
    named_entities_str_tag = [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities]

    print(named_entities_str_tag)


    return render_template('output.html',
                            output=request.args.get("output", output),
                            question=request.args.get("question", question))

if __name__ == '__main__':
    app.run()
