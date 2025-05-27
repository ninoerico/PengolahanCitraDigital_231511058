from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import numpy as np
import os
from utils import read_uploaded_file  # Import langsung dari utils

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def rgb_array_page(request: Request):
    return templates.TemplateResponse("rgb_array.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def rgb_array_operation(request: Request, file: UploadFile = File(...)):
    try:
        # Baca file gambar (TIDAK menggunakan await karena read_uploaded_file bukan async)
        img = read_uploaded_file(file)
        if img is None:
            return templates.TemplateResponse("error.html", {
                "request": request,
                "message": "Tidak dapat membaca gambar yang diunggah"
            })

        # Konversi array gambar ke string untuk ditampilkan
        # Limit ukuran array untuk display (agar tidak terlalu besar)
        if img.size > 50000:  # Jika gambar terlalu besar
            # Resize untuk display
            import cv2
            resized_img = cv2.resize(img, (50, 50))
            rgb_array_str = np.array2string(resized_img, separator=', ', threshold=1000)
            message = f"Gambar terlalu besar, menampilkan sample 50x50 pixel pertama"
        else:
            rgb_array_str = np.array2string(img, separator=', ', threshold=1000)
            message = "Array RGB lengkap"

        return templates.TemplateResponse("rgb_array_result.html", {
            "request": request,
            "rgb_array": rgb_array_str,
            "message": message,
            "input_url": "/rgb_array/"
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": f"Error memproses gambar: {str(e)}"
        })