from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes import grayscale, histogram, equalize, specify, arithmetic, logic, convolution, fourier, noise_reduction, statistics, rgb_array, zero_padding, filter, periodic_noise

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(grayscale.router, prefix="/grayscale")
app.include_router(histogram.router, prefix="/histogram")
app.include_router(equalize.router, prefix="/equalize")
app.include_router(specify.router, prefix="/specify")
app.include_router(arithmetic.router, prefix="/arithmetic")
app.include_router(logic.router, prefix="/logic")
app.include_router(convolution.router, prefix="/convolution")
app.include_router(fourier.router, prefix="/fourier")
app.include_router(noise_reduction.router, prefix="/noise_reduction")
app.include_router(statistics.router, prefix="/statistics")
app.include_router(rgb_array.router, prefix="/rgb_array")
app.include_router(zero_padding.router, prefix="/zero_padding")
app.include_router(filter.router, prefix="/filter")
app.include_router(periodic_noise.router, prefix="/periodic_noise")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Home endpoint
@app.get("/")
async def home(request: Request):
    logger.info("Mengakses endpoint utama: /")
    try:
        return templates.TemplateResponse("home.html", {"request": request})
    except Exception as e:
        logger.error(f"Error saat merender home.html: {e}")
        raise