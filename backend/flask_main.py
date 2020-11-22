from flask import Flask, render_template, request
import wikipedia
app = Flask(__name__)


def link_entities(question):

    e = open("entities.txt", "r")
    content = e.read()
    entities = content.split("\n")[:-1]
    e.close()

    entity_map = dict()

    print(question)

    for word in question.split():
        print("word: " + str(word))
        try:
            search_term = wikipedia.page(word)
            related = search_term.links
            suggestions = list(set(related) & set(entities))
            if(suggestions != []):
                entity_map[word] = suggestions
        except:
            continue


    return entity_map
    # entity_list = entity_map.values()
    # entity_str = ""
    #
    # for e in entity_list:
    #     entity_str += str(e) + "\n"
    #
    # return entity_str

@app.route('/')
def hello():
    return render_template('pastIndex.html')

@app.route('/link', methods=['GET','POST'])
def main():
    question = request.form.get("textInput", 0)
    reverseTxt = "dkjldfsjlkfsd"

    output = str(link_entities(question))

    return render_template('output.html',
                            output=request.args.get("output", output),
                            question=request.args.get("question", question))

if __name__ == '__main__':
    app.run()
