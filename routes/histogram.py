from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import read_uploaded_file, save_image, save_histogram

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def histogram_page(request: Request):
    return templates.TemplateResponse("histogram.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def histogram_operation(request: Request, file: UploadFile = File(...)):
    img = read_uploaded_file(file)
    if img is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "Tidak dapat membaca gambar yang diunggah"
        })
    
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    original_path = save_image(img, "original")
    grayscale_histogram_path = save_histogram(gray_img, "grayscale_histogram")
    color_histogram_path = save_histogram(img, "color_histogram", grayscale=False)
    
    return templates.TemplateResponse("histogram_result.html", {
        "request": request,
        "original_image_path": original_path,
        "grayscale_histogram_path": grayscale_histogram_path,
        "color_histogram_path": color_histogram_path,
        "input_url": "/histogram/"
    })