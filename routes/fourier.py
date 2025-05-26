from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import cv2
import numpy as np
from utils import read_uploaded_file, save_image

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def fourier_page(request: Request):
    return templates.TemplateResponse("fourier.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def fourier_operation(request: Request, file: UploadFile = File(...)):
    img = read_uploaded_file(file)
    if img is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "Tidak dapat membaca gambar yang diunggah"
        })
    
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    f = np.fft.fft2(gray_img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
    magnitude_spectrum = np.asarray(magnitude_spectrum, dtype=np.uint8)
    magnitude_spectrum = cv2.cvtColor(magnitude_spectrum, cv2.COLOR_GRAY2BGR)
    
    original_path = save_image(img, "original")
    modified_path = save_image(magnitude_spectrum, "modified")
    
    return templates.TemplateResponse("result.html", {
        "request": request,
        "original_image_path": original_path,
        "modified_image_path": modified_path,
        "input_url": "/fourier/"
    })