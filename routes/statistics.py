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
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mean_intensity = np.mean(gray_img)
    std_deviation = np.std(gray_img)
    image_path = save_image(img, "original")
    return templates.TemplateResponse("statistics.html", {
        "request": request,
        "image_path": image_path,
        "mean_intensity": round(mean_intensity, 2),
        "std_deviation": round(std_deviation, 2)
    })