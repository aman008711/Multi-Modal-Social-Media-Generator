from fastapi import FastAPI
from pydantic import BaseModel
from app.services.week4_image_generator import generate_image

app = FastAPI(title="Multi-Modal Social Media Generator API")

# Input model
class ImageRequest(BaseModel):
    brief: str
    style: str = "product_ad"
    quality: str = "high"

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Multi-Modal Social Media Generator API!"}

# Result endpoint
@app.post("/result")
def generate_result(request: ImageRequest):
    """
    Input: User brief, style, quality
    Output: Path to generated image
    """
    image_path = generate_image(request.brief, style=request.style, quality=request.quality)
    return {
        "brief": request.brief,
        "style": request.style,
        "quality": request.quality,
        "image_path": image_path
    }