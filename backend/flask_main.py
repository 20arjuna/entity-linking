from flask import Flask,render_template, Response, request, redirect, url_for, send_file
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('pastIndex.html')

if __name__ == '__main__':
    app.run()
