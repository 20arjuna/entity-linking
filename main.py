from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates/")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/link/")
def entity_link(request: Request, textInput: str = Form(...)):
    print("did it reach here?")
    display_output(Request, textInput)
    # print(textInput)
    # return templates.TemplateResponse("index.html", context={'request': Request, 'result': result})

@app.post("/result")
def display_output(request: Request, input_string):
    print(input_string)
    return [{"result": input_string}]