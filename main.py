from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
#from src.model import spell_number

app = FastAPI()
templates = Jinja2Templates(directory="templates/")

@app.route('/')
def hello():
    return templates.TemplateResponse('frontend.html')

@app.get("/form")
def form_post(request: Request):
    result = "Type a number"
    return templates.TemplateResponse('sample.html', context={'request': request, 'result': result})


@app.post("/form")
def form_post(request: Request, num: int = Form(...)):
    result = "bub"
    return templates.TemplateResponse('sample.html', context={'request': request, 'result': result})