from fastapi import FastAPI, Request, Form, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates/")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    #print(request)
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/link")
def entity_link(textInput: str = Form(...)):
    print("got here")
    payload = {"entities" : textInput}
    return payload

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         await asyncio.sleep(0.1)
#         payload = next(measurements)
#         await websocket.send_json(payload)