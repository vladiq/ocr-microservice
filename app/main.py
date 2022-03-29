import pathlib

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = pathlib.Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
def home_view(request: Request): #http GET -> return JSON
    print(request)
    return templates.TemplateResponse(
        'home.html',
        {'request': request}
    )

@app.post('/')
def home_detail_view():
    return {'hello' : 'world'}
