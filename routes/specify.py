from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import numpy as np
from skimage.exposure import match_histograms
from utils import read_uploaded_file, save_image

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def specify_page(request: Request):
    return templates.TemplateResponse("specify.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def histogram_specification(request: Request, file: UploadFile = File(...), ref_file: UploadFile = File(...)):
    img = read_uploaded_file(file)
    ref_img = read_uploaded_file(ref_file)
    if img is None or ref_img is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "Tidak dapat membaca salah satu gambar yang diunggah"
        })
    
    matched_img = match_histograms(img, ref_img, multichannel=True)
    matched_img = np.asarray(matched_img, dtype=np.uint8)
    
    original_path = save_image(img, "original")
    reference_path = save_image(ref_img, "reference")
    modified_path = save_image(matched_img, "modified")
    
    return templates.TemplateResponse("specify_result.html", {
        "request": request,
        "original_image_path": original_path,
        "reference_image_path": reference_path,
        "modified_image_path": modified_path,
        "input_url": "/specify/"
    })