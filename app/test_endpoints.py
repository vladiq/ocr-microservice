import io
from fastapi.testclient import TestClient
from PIL import Image, ImageChops

from app.main import app, BASE_DIR

client = TestClient(app)

def test_get_home() -> None:
    response = client.get('/')
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']

def test_prediction_upload() -> None:
    img_saved_path = BASE_DIR / 'uploaded'
    for path in img_saved_path.glob('*'):
        try:
            img = Image.open(path)
        except:
            img = None

        response = client.post('/', files={'file': open(path,'rb')})
        if img is None:
            assert response.status_code == 400
        else:
            # Returning a valid image
            assert response.status_code == 200
            data = response.json()
            assert len(data.keys()) == 1

def test_echo_upload() -> None:
    img_saved_path = BASE_DIR / 'uploaded'
    for path in img_saved_path.glob('*'):
        try:
            img = Image.open(path)
        except:
            img = None

        response = client.post('/img-echo', files={'file': open(path,'rb')})
        if img is None:
            assert response.status_code == 400
        else:
            # Returning a valid image
            assert response.status_code == 200
            r_stream = io.BytesIO(response.content)
            echo_img = Image.open(r_stream)
            difference = ImageChops.difference(echo_img, img).getbbox()
            assert difference is None