from flask import Flask, render_template, request,
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('pastIndex.html')

@app.route('/link', methods=['GET','POST'])
def main():
    question = request.form.get("textInput", 0)
    reverseTxt = text[::-1]
    return render_template('output.html',
                            output=request.args.get("output", reverseTxt),
                            question=request.args.get("question", text))


if __name__ == '__main__':
    app.run()
