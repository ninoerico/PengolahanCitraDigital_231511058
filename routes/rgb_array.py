from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import numpy as np
from utils import read_uploaded_file

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def rgb_array_page(request: Request):
    return templates.TemplateResponse("rgb_array.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def rgb_array_operation(request: Request, file: UploadFile = File(...)):
    img = read_uploaded_file(file)
    if img is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "Tidak dapat membaca gambar yang diunggah"
        })
    
    # Konversi array gambar ke string untuk ditampilkan
    rgb_array_str = np.array2string(img, separator=', ')
    
    return templates.TemplateResponse("rgb_array.html", {
        "request": request,
        "rgb_array": rgb_array_str
    })