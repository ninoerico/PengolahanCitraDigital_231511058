from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import cv2
from utils import read_uploaded_file, save_image

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def noise_reduction_page(request: Request):
    return templates.TemplateResponse("noise_reduction.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def noise_reduction_operation(request: Request, file: UploadFile = File(...)):
    img = read_uploaded_file(file)
    if img is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "Tidak dapat membaca gambar yang diunggah"
        })
    
    denoised_img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    original_path = save_image(img, "original")
    modified_path = save_image(denoised_img, "modified")
    
    return templates.TemplateResponse("result.html", {
        "request": request,
        "original_image_path": original_path,
        "modified_image_path": modified_path,
        "input_url": "/noise_reduction/"
    })