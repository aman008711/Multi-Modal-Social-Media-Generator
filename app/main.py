"""
FastAPI Application for Marketing Caption Generator
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from app.services.caption_generator import get_caption_generator, initialize_caption_generator
from app.services.image_generator import get_image_generator, initialize_image_generator
from app.utils.brand_personas import list_personas
import os

app = FastAPI(
    title="Multi-Modal Social Media Generator",
    description="Generate marketing captions using Phi-2 LLM and AI-generated images using Stable Diffusion",
    version="2.0.0"
)

# Pydantic models for request/response
class CaptionRequest(BaseModel):
    product_description: str
    persona_key: str
    num_captions: int = 1

class MultiPersonaCaptionRequest(BaseModel):
    product_description: str
    personas: Optional[List[str]] = None
    num_captions_per_persona: int = 2

class CaptionResponse(BaseModel):
    product_description: str
    persona_key: str
    captions: List[str]

class MultiPersonaCaptionResponse(BaseModel):
    product_description: str
    results: dict

# Image Generation Models
class ImageGenerationRequest(BaseModel):
    user_brief: str
    style: str = "product_ad"  # product_ad, lifestyle, minimalist, vibrant, luxury
    quality: str = "high"  # low, medium, high, ultra
    num_inference_steps: int = 50

class ImageGenerationResponse(BaseModel):
    success: bool = True
    user_brief: str
    enhanced_prompt: str
    image_path: str
    style: str
    quality: str
    image_format: str = "PNG"
    image_size: str = "512x512"

# Initialize the caption generator on startup
@app.on_event("startup")
async def startup_event():
    """Initialize models on app startup"""
    try:
        initialize_caption_generator()
        print("Caption generator initialized successfully!")
    except Exception as e:
        print(f"Warning: Caption generator initialization delayed - {e}")
        print("Model will be loaded on first request")
    
    try:
        initialize_image_generator()
        print("Image generator initialized successfully!")
    except Exception as e:
        print(f"Warning: Image generator initialization delayed - {e}")
        print("Model will be loaded on first request")

# Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Multi-Modal Social Media Generator API",
        "version": "2.0.0",
        "endpoints": {
            "captions": {
                "generate_caption": "/generate-caption",
                "generate_multi_persona": "/generate-multi-persona",
                "list_personas": "/personas"
            },
            "images": {
                "generate_image": "/generate-image",
                "download_image": "/download-image/{filename}"
            },
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/personas")
async def get_personas():
    """Get list of available brand personas"""
    return {
        "personas": list_personas(),
        "count": len(list_personas())
    }

@app.post("/generate-caption", response_model=CaptionResponse)
async def generate_caption(request: CaptionRequest):
    """
    Generate marketing captions for a product
    
    - **product_description**: Description of the product
    - **persona_key**: Brand persona to use (e.g., 'luxury_brand', 'tech_startup')
    - **num_captions**: Number of captions to generate (default: 1)
    """
    try:
        # Validate persona
        if request.persona_key not in list_personas():
            raise HTTPException(
                status_code=400,
                detail=f"Unknown persona: {request.persona_key}. Available: {list_personas()}"
            )
        
        # Generate captions
        generator = get_caption_generator()
        captions = generator.generate_caption(
            request.product_description,
            request.persona_key,
            request.num_captions
        )
        
        if isinstance(captions, dict) and "error" in captions:
            raise HTTPException(status_code=400, detail=captions["error"])
        
        return CaptionResponse(
            product_description=request.product_description,
            persona_key=request.persona_key,
            captions=captions
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-multi-persona", response_model=MultiPersonaCaptionResponse)
async def generate_multi_persona_captions(request: MultiPersonaCaptionRequest):
    """
    Generate captions for multiple brand personas
    
    - **product_description**: Description of the product
    - **personas**: List of persona keys to use (if None, uses all personas)
    - **num_captions_per_persona**: Number of captions per persona (default: 2)
    """
    try:
        generator = get_caption_generator()
        
        # Validate personas if provided
        if request.personas:
            invalid_personas = [p for p in request.personas if p not in list_personas()]
            if invalid_personas:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unknown personas: {invalid_personas}. Available: {list_personas()}"
                )
        
        # Generate captions for all or specified personas
        results = {}
        personas_to_use = request.personas or list_personas()
        
        for persona_key in personas_to_use:
            captions = generator.generate_caption(
                request.product_description,
                persona_key,
                request.num_captions_per_persona
            )
            results[persona_key] = captions
        
        return MultiPersonaCaptionResponse(
            product_description=request.product_description,
            results=results
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Image Generation Endpoints
@app.post("/generate-image", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest):
    """
    Generate an AI image from a user brief
    
    - **user_brief**: Simple product description (e.g., 'Red running shoes')
    - **style**: Image style - product_ad, lifestyle, minimalist, vibrant, luxury
    - **quality**: Quality level - low, medium, high, ultra
    - **num_inference_steps**: Inference steps for quality (default: 50, higher = better)
    """
    try:
        # Generate image
        generator = get_image_generator()
        result = generator.generate_image(
            user_brief=request.user_brief,
            style=request.style,
            quality=request.quality,
            num_inference_steps=request.num_inference_steps,
            output_dir="generated_images"
        )
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return ImageGenerationResponse(
            success=result.get("success", True),
            user_brief=result.get("user_brief"),
            enhanced_prompt=result.get("enhanced_prompt"),
            image_path=result.get("image_path"),
            style=result.get("style"),
            quality=result.get("quality"),
            image_format=result.get("image_format", "PNG"),
            image_size=result.get("image_size", "512x512")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download-image/{filename}")
async def download_image(filename: str):
    """
    Download a generated image by filename
    
    - **filename**: Name of the image file (without path)
    """
    try:
        filepath = os.path.join("generated_images", filename)
        
        # Security check: ensure file is in generated_images directory
        filepath = os.path.abspath(filepath)
        generated_dir = os.path.abspath("generated_images")
        
        if not filepath.startswith(generated_dir):
            raise HTTPException(status_code=403, detail="Access denied")
        
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Image not found")
        
        return FileResponse(
            filepath,
            media_type="image/png",
            filename=filename
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


from fastapi import FastAPI
from app.celery_worker import celery_app
from app.services.image_tasks import generate_image_task

app = FastAPI()

@app.post("/generate-image")
def generate_image(request: dict):
    task = generate_image_task.delay(request)

    return {
        "message": "Image generation started",
        "job_id": task.id
    }

@app.get("/result/{job_id}")
def get_result(job_id: str):
    result = celery_app.AsyncResult(job_id)

    if result.state == "PENDING":
        return {"status": "Processing..."}

    elif result.state == "SUCCESS":
        return result.result

    elif result.state == "FAILURE":
        return {
            "status":"Failed",
            "error":str(result.result)
        }
    return {"status": result.state}