from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import logging

# Import semua router - import langsung router object
from routes.arithmetic import router as arithmetic_router
from routes.logic import router as logic_router
from routes.grayscale import router as grayscale_router
from routes.histogram import router as histogram_router
from routes.equalize import router as equalize_router
from routes.specify import router as specify_router
from routes.convolution import router as convolution_router
from routes.fourier import router as fourier_router
from routes.noise_reduction import router as noise_reduction_router
from routes.statistics import router as statistics_router
from routes.rgb_array import router as rgb_array_router
from routes.zero_padding import router as zero_padding_router
from routes.filter import router as filter_router
from routes.periodic_noise import router as periodic_noise_router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Image Processing API", version="1.0.0")

# Mount static files - pastikan path relatif benar
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include all routers
app.include_router(arithmetic_router, prefix="/arithmetic", tags=["arithmetic"])
app.include_router(logic_router, prefix="/logic", tags=["logic"])
app.include_router(grayscale_router, prefix="/grayscale", tags=["grayscale"])
app.include_router(histogram_router, prefix="/histogram", tags=["histogram"])
app.include_router(equalize_router, prefix="/equalize", tags=["equalize"])
app.include_router(specify_router, prefix="/specify", tags=["specify"])
app.include_router(convolution_router, prefix="/convolution", tags=["convolution"])
app.include_router(fourier_router, prefix="/fourier", tags=["fourier"])
app.include_router(noise_reduction_router, prefix="/noise_reduction", tags=["noise_reduction"])
app.include_router(statistics_router, prefix="/statistics", tags=["statistics"])
app.include_router(rgb_array_router, prefix="/rgb_array", tags=["rgb_array"])
app.include_router(zero_padding_router, prefix="/zero_padding", tags=["zero_padding"])
app.include_router(filter_router, prefix="/filter", tags=["filter"])
app.include_router(periodic_noise_router, prefix="/periodic_noise", tags=["periodic_noise"])

# Home endpoint
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    logger.info("Mengakses endpoint utama: /")
    try:
        return templates.TemplateResponse("home.html", {"request": request})
    except Exception as e:
        logger.error(f"Error saat merender home.html: {e}")
        raise

# Handler untuk Vercel (jika diperlukan di masa depan)
# Tapi untuk localhost, gunakan uvicorn di bawah
handler = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)