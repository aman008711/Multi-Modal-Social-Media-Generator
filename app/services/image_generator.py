"""
Image Generation Service using Stable Diffusion
"""

from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import os
from datetime import datetime
from app.utils.prompt_enhancer import get_prompt_enhancer

class ImageGenerator:
    """Generate images from text prompts using Stable Diffusion"""
    
    def __init__(self, model_id: str = "runwayml/stable-diffusion-v1-5"):
        self.model_id = model_id
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipeline = None
        self.prompt_enhancer = get_prompt_enhancer()
        
    def initialize(self):
        """Initialize the Stable Diffusion pipeline"""
        try:
            print(f"Loading Stable Diffusion model on device: {self.device}")
            
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None  # Disable safety checker for faster inference
            )
            self.pipeline.to(self.device)
            
            # Enable memory optimization
            if self.device == "cuda":
                self.pipeline.enable_attention_slicing()
            
            print("Stable Diffusion model loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading Stable Diffusion model: {e}")
            return False
    
    def generate_image(self, 
                      user_brief: str,
                      style: str = "product_ad",
                      quality: str = "high",
                      num_inference_steps: int = 50,
                      guidance_scale: float = 7.5,
                      output_dir: str = "generated_images") -> dict:
        """
        Generate an image from a user brief
        
        Args:
            user_brief: User's product description (e.g., "Red running shoes")
            style: Image style (product_ad, lifestyle, minimalist, vibrant, luxury)
            quality: Quality level (low, medium, high, ultra)
            num_inference_steps: Number of inference steps (higher = better quality, slower)
            guidance_scale: Guidance scale for prompt adherence (7.5 is default)
            output_dir: Directory to save generated images
            
        Returns:
            Dictionary with image path, prompt, and metadata
        """
        
        if self.pipeline is None:
            try:
                self.initialize()
            except Exception as e:
                return {"error": f"Image generator not available: {str(e)}"}
        
        try:
            # Enhance the prompt
            enhanced_prompt = self.prompt_enhancer.enhance_prompt(
                user_brief, 
                style=style,
                quality=quality
            )
            
            print(f"User Brief: {user_brief}")
            print(f"Enhanced Prompt: {enhanced_prompt}")
            
            # Generate image
            with torch.no_grad():
                image = self.pipeline(
                    prompt=enhanced_prompt,
                    height=512,
                    width=512,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale
                ).images[0]
            
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{user_brief.replace(' ', '_')}_{timestamp}.png"
            filepath = os.path.join(output_dir, filename)
            image.save(filepath)
            
            return {
                "success": True,
                "user_brief": user_brief,
                "enhanced_prompt": enhanced_prompt,
                "image_path": filepath,
                "style": style,
                "quality": quality,
                "image_format": "PNG",
                "image_size": "512x512",
                "inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale
            }
            
        except Exception as e:
            print(f"Error generating image: {e}")
            return {
                "error": str(e),
                "user_brief": user_brief,
                "enhanced_prompt": enhanced_prompt if hasattr(self, 'enhanced_prompt') else None
            }
    
    def batch_generate_images(self,
                             briefs: list,
                             style: str = "product_ad",
                             quality: str = "high",
                             num_inference_steps: int = 50,
                             output_dir: str = "generated_images") -> list:
        """
        Generate images for multiple briefs
        
        Args:
            briefs: List of user briefs
            style: Image style for all
            quality: Quality level for all
            num_inference_steps: Inference steps for all
            output_dir: Output directory
            
        Returns:
            List of generation results
        """
        results = []
        for i, brief in enumerate(briefs):
            print(f"Generating image {i+1}/{len(briefs)}: {brief}")
            result = self.generate_image(
                brief,
                style=style,
                quality=quality,
                num_inference_steps=num_inference_steps,
                output_dir=output_dir
            )
            results.append(result)
        
        return results
    
    def unload_model(self):
        """Unload the model to free memory"""
        self.pipeline = None
        torch.cuda.empty_cache()
        print("Model unloaded and memory cleared.")


# Create a global instance
_image_generator = None

def get_image_generator() -> ImageGenerator:
    """Get or create the image generator instance"""
    global _image_generator
    if _image_generator is None:
        _image_generator = ImageGenerator()
    return _image_generator

def initialize_image_generator():
    """Initialize the image generator"""
    generator = get_image_generator()
    return generator.initialize()
