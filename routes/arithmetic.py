from fastapi import APIRouter, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import cv2
import numpy as np
from utils import read_uploaded_file, save_image

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def arithmetic_page(request: Request):
    return templates.TemplateResponse("arithmetic.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def arithmetic_operations(request: Request, file: UploadFile = File(...), operation: str = Form(...), value: int = Form(0)):
    img = read_uploaded_file(file)
    if img is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "Tidak dapat membaca gambar yang diunggah"
        })
    
    if operation == "add":
        modified_img = cv2.add(img, np.array([value, value, value], dtype=np.uint8))
    elif operation == "subtract":
        modified_img = cv2.subtract(img, np.array([value, value, value], dtype=np.uint8))
    elif operation == "max":
        modified_img = np.maximum(img, np.array([value, value, value], dtype=np.uint8))
    elif operation == "min":
        modified_img = np.minimum(img, np.array([value, value, value], dtype=np.uint8))
    elif operation == "inverse":
        modified_img = 255 - img
    else:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "Operasi tidak valid"
        })
    
    original_path = save_image(img, "original")
    modified_path = save_image(modified_img, "modified")
    
    return templates.TemplateResponse("result.html", {
        "request": request,
        "original_image_path": original_path,
        "modified_image_path": modified_path,
        "input_url": "/arithmetic/"
    })