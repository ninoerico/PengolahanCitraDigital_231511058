from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import numpy as np
import cv2
from utils import read_uploaded_file, save_image

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def statistics_page(request: Request):
    return templates.TemplateResponse("statistics.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def statistics_operation(request: Request, file: UploadFile = File(...)):
    img = read_uploaded_file(file)
    
    # Error handling - cek jika gambar tidak bisa dibaca
    if img is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "Tidak dapat membaca gambar yang diunggah"
        })
    
    try:
        # Convert to grayscale untuk analisis statistik
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Hitung statistik
        mean_intensity = np.mean(gray_img)
        std_deviation = np.std(gray_img)
        min_intensity = np.min(gray_img)
        max_intensity = np.max(gray_img)
        median_intensity = np.median(gray_img)
        
        # Save original image
        image_path = save_image(img, "original")
        
        return templates.TemplateResponse("statistics_result.html", {
            "request": request,
            "image_path": image_path,
            "mean_intensity": round(mean_intensity, 2),
            "std_deviation": round(std_deviation, 2),
            "min_intensity": int(min_intensity),
            "max_intensity": int(max_intensity),
            "median_intensity": round(median_intensity, 2),
            "input_url": "/statistics/"
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": f"Error menghitung statistik gambar: {str(e)}"
        })