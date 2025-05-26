from fastapi import APIRouter, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import cv2
import numpy as np
from utils import read_uploaded_file, save_image

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def convolution_page(request: Request):
    return templates.TemplateResponse("convolution.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def convolution_operation(request: Request, file: UploadFile = File(...), kernel_type: str = Form(...)):
    img = read_uploaded_file(file)
    if img is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "Tidak dapat membaca gambar yang diunggah"
        })
    
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if kernel_type == "average":
        kernel = np.ones((3, 3), np.float32) / 9
    elif kernel_type == "sharpen":
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    elif kernel_type == "edge":
        kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    else:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "Tipe kernel tidak valid"
        })
    
    modified_img = cv2.filter2D(gray_img, -1, kernel)
    modified_img = cv2.cvtColor(modified_img, cv2.COLOR_GRAY2BGR)
    
    original_path = save_image(img, "original")
    modified_path = save_image(modified_img, "modified")
    
    return templates.TemplateResponse("result.html", {
        "request": request,
        "original_image_path": original_path,
        "modified_image_path": modified_path,
        "input_url": "/convolution/"
    })