from fastapi import APIRouter, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import cv2
from utils import read_uploaded_file, save_image

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def zero_padding_page(request: Request):
    return templates.TemplateResponse("zero_padding.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def zero_padding_operation(request: Request, file: UploadFile = File(...), padding_size: int = Form(10)):
    img = read_uploaded_file(file)
    if img is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "Tidak dapat membaca gambar yang diunggah"
        })
    
    if padding_size < 0 or padding_size > 100:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "Ukuran padding harus antara 0 dan 100"
        })
    
    padded_img = cv2.copyMakeBorder(img, padding_size, padding_size, padding_size, padding_size, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    
    original_path = save_image(img, "original")
    modified_path = save_image(padded_img, "modified")
    
    return templates.TemplateResponse("result.html", {
        "request": request,
        "original_image_path": original_path,
        "modified_image_path": modified_path,
        "input_url": "/zero_padding/"
    })