from fastapi import APIRouter, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import cv2
import numpy as np
from utils import read_uploaded_file, save_image

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def filter_page(request: Request):
    return templates.TemplateResponse("filter.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def filter_operation(request: Request, file: UploadFile = File(...), filter_type: str = Form(...)):
    img = read_uploaded_file(file)
    if img is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "Tidak dapat membaca gambar yang diunggah"
        })
    
    if filter_type == "low":
        filtered_img = cv2.GaussianBlur(img, (5, 5), 0)
    elif filter_type == "high":
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        filtered_img = cv2.filter2D(img, -1, kernel)
    elif filter_type == "band":
        low_pass = cv2.GaussianBlur(img, (9, 9), 0)
        high_pass = img - low_pass
        filtered_img = low_pass + high_pass
    else:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "Tipe filter tidak valid"
        })
    
    original_path = save_image(img, "original")
    modified_path = save_image(filtered_img, "modified")
    
    return templates.TemplateResponse("result.html", {
        "request": request,
        "original_image_path": original_path,
        "modified_image_path": modified_path,
        "input_url": "/filter/"
    })