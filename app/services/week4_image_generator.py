"""
Week 4: Image Generator with Prompt Enhancer and Post-Processing
"""

import io
from PIL import Image, ImageDraw, ImageFont
from app.utils.prompt_enhancer import get_prompt_enhancer

# Replace this with your actual model import
# from app.models import image_model as model

# Mock model for demonstration (replace with your model)
class MockModel:
    def generate(self, prompt: str):
        print(f"[Model] Generating image for prompt:\n{prompt}\n")
        img = Image.new("RGB", (512, 512), color="white")  # blank image
        bytes_io = io.BytesIO()
        img.save(bytes_io, format="PNG")
        return bytes_io.getvalue()

model = MockModel()

prompt_enhancer = get_prompt_enhancer()


def generate_image(user_brief: str, style: str = "product_ad", quality: str = "high") -> str:
    # Step 1: Enhance prompt
    enhanced_prompt = prompt_enhancer.enhance_prompt(user_brief, style=style, quality=quality)
    print(f"[Prompt Enhancer] Enhanced Prompt:\n{enhanced_prompt}\n")

    # Step 2: Generate image
    image_bytes = model.generate(enhanced_prompt)
    image = Image.open(io.BytesIO(image_bytes))

    # Step 3: Post-processing
    image = image.resize((1024, 1024))
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()
    draw.text((10, 10), "My Social Media", fill="white", font=font)

    # Step 4: Save final image
    output_path = f"output_{user_brief.replace(' ', '_')}.png"
    image.save(output_path)
    print(f"[Image Generator] Saved final image: {output_path}")

    return output_path


if __name__ == "__main__":
    # Example usage
    briefs = ["Red running shoes", "Blue leather handbag", "Smartphone with sleek design"]
    for brief in briefs:
        generate_image(brief, style="product_ad", quality="high")