import pathlib
import io
import uuid
from pydantic import BaseSettings
from functools import lru_cache
from PIL import Image
import pytesseract

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    Depends,
    File,
    UploadFile
)
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

class Settings(BaseSettings):
    debug: bool = False
    echo_active: bool = False

    class Config:
        env_file: str = '.env'

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
DEBUG = settings.debug
BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / 'uploaded'
templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
def home_view(request: Request, settings: Settings = Depends(get_settings)):
    return templates.TemplateResponse(
        'home.html',
        {'request': request}
    )

@app.post('/', response_class=FileResponse)
async def prediction_view(
    file: UploadFile = File(...),
    settings: Settings = Depends(get_settings)
):

    if not settings.echo_active:
        raise HTTPException(detail='Invalid endpoint', status_code=400)
    UPLOAD_DIR.mkdir(exist_ok=True)
    file_bytes = await file.read()
    bytes_str = io.BytesIO(file_bytes)
    try:
        img = Image.open(bytes_str)
    except:
        raise HTTPException(detail="Invalid image", status_code=400)

    predictions = pytesseract.image_to_string(img).split('\n')
    return {'result': predictions}

@app.post('/img-echo', response_class=FileResponse)
async def img_echo_view(
    file: UploadFile = File(...),
    settings: Settings = Depends(get_settings)
):

    if not settings.echo_active:
        raise HTTPException(detail='Invalid endpoint', status_code=400)
    UPLOAD_DIR.mkdir(exist_ok=True)
    file_bytes = await file.read()
    bytes_str = io.BytesIO(file_bytes)

    try:
        img = Image.open(bytes_str)
    except:
        raise HTTPException(detail="Invalid image", status_code=400)

    filename = pathlib.Path(file.filename)
    fext = filename.suffix
    dest = UPLOAD_DIR / f'{uuid.uuid1()}{fext}'
    img.save(dest)
    return dest