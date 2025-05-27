from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import cv2
import numpy as np
from utils import read_uploaded_file, save_image

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def equalize_page(request: Request):
    return templates.TemplateResponse("equalize.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def equalize_operation(request: Request, file: UploadFile = File(...)):
    img = read_uploaded_file(file)
    if img is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "Tidak dapat membaca gambar yang diunggah"
        })

    # Convert to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply histogram equalization
    equalized_img = cv2.equalizeHist(gray_img)
    
    # Convert back to BGR for consistency
    equalized_img = cv2.cvtColor(equalized_img, cv2.COLOR_GRAY2BGR)

    # Save images
    original_path = save_image(img, "original")
    modified_path = save_image(equalized_img, "modified")

    return templates.TemplateResponse("result.html", {
        "request": request,
        "original_image_path": original_path,
        "modified_image_path": modified_path,
        "input_url": "/equalize/"
    })