from fastapi import APIRouter, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import cv2
import numpy as np
from utils import read_uploaded_file, save_image

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def logic_page(request: Request):
    return templates.TemplateResponse("logic.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def logic_operations(request: Request, file1: UploadFile = File(...), file2: UploadFile = File(None), operation: str = Form(...)):
    img1 = read_uploaded_file(file1)
    if img1 is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "Tidak dapat membaca gambar pertama"
        })
    
    if operation in ["and", "xor"] and file2 is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "Operasi AND dan XOR memerlukan dua gambar"
        })
    
    if operation == "not":
        modified_img = cv2.bitwise_not(img1)
    else:
        img2 = read_uploaded_file(file2)
        if img2 is None:
            return templates.TemplateResponse("error.html", {
                "request": request,
                "message": "Tidak dapat membaca gambar kedua"
            })
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        if operation == "and":
            modified_img = cv2.bitwise_and(img1, img2)
        elif operation == "xor":
            modified_img = cv2.bitwise_xor(img1, img2)
        else:
            return templates.TemplateResponse("error.html", {
                "request": request,
                "message": "Operasi tidak valid"
            })
    
    original_path = save_image(img1, "original")
    modified_path = save_image(modified_img, "modified")
    
    return templates.TemplateResponse("result.html", {
        "request": request,
        "original_image_path": original_path,
        "modified_image_path": modified_path,
        "input_url": "/logic/"
    })