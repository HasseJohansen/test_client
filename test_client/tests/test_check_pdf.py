from test_client.app import check_pdf, api
from fastapi.testclient import TestClient
from PIL import Image
from random import seed
from random import randint
import io

client = TestClient(api)

def get_random_int():
    return randint(1, 529852)

def check_png(png_data):
    try:
        im=Image.open(io.BytesIO(png_data))
        return True if im.format == "PNG" else False
    except IOError:
        return False


def test_check_valid_pdf():
    with open("tests/fixtures/dummy.pdf", "rb") as f:
        pdf_file = f.read()
        assert check_pdf(pdf_file) == True

def test_check_invalid_pdf():
    with open("tests/fixtures/corrupt-dummy.pdf", "rb") as f:
        pdf_file = f.read()
        assert check_pdf(pdf_file) == False

def test_api_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "Healthy"}

def test_api_get_from_dummy_valid_pdf():
    while True:
        response = client.get(f"/{get_random_int()}")
        if response.status_code == 200 and response.headers.get("Content-Type") == "application/pdf":
            assert check_pdf(response.content) == True
            break

def test_api_get_from_dummy_valid_png():
    while True:
        response = client.get(f"/{get_random_int()}")
        if response.status_code == 200 and response.headers.get("Content-Type") == "image/png":
            assert check_png(response.content) == True
            break

def test_api_get_from_dummy_invalid_pdf():
    while True:
        response = client.get(f"/{get_random_int()}")
        if response.status_code == 204:
            assert response.content == b''
            break
        
        
