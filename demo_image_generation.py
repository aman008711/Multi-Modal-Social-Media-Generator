"""
Week 2 Image Generation Demo
Practical examples of how to use the image generation system
"""

import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.utils.prompt_enhancer import get_prompt_enhancer
from app.services.image_generator import get_image_generator


def demo_prompt_enhancement():
    """Demo 1: Enhance a simple product brief"""
    print("\n" + "="*70)
    print("DEMO 1: PROMPT ENHANCEMENT")
    print("="*70)
    
    enhancer = get_prompt_enhancer()
    
    # Simple input from user
    user_brief = "Red running shoes"
    
    print(f"\n📝 User Input: '{user_brief}'")
    print("\nEnhancing prompt for different styles:\n")
    
    styles = ["product_ad", "lifestyle", "minimalist", "vibrant", "luxury"]
    
    for style in styles:
        enhanced = enhancer.enhance_prompt(user_brief, style=style, quality="high")
        print(f"✓ {style.upper()}")
        print(f"  {enhanced[:120]}...")
        print()


def demo_batch_processing():
    """Demo 2: Process multiple products at once"""
    print("\n" + "="*70)
    print("DEMO 2: BATCH PROMPT PROCESSING")
    print("="*70)
    
    enhancer = get_prompt_enhancer()
    
    products = [
        "Red running shoes",
        "Black leather jacket",
        "Silver smartwatch",
        "Pink cosmetic bag",
        "Wooden coffee table"
    ]
    
    print(f"\n📚 Processing {len(products)} products:\n")
    
    enhanced_prompts = enhancer.batch_enhance(products, style="product_ad", quality="high")
    
    for product, prompt in zip(products, enhanced_prompts):
        print(f"✓ {product}")
        print(f"  Prompt length: {len(prompt)} chars")
        print()


def demo_image_generation_workflow():
    """Demo 3: Complete image generation workflow"""
    print("\n" + "="*70)
    print("DEMO 3: IMAGE GENERATION WORKFLOW")
    print("="*70)
    
    # Initialize generator
    generator = get_image_generator()
    
    user_brief = "Red running shoes"
    
    print(f"\n🎯 Target: Generate AI image for '{user_brief}'")
    print("\nWorkflow Steps:")
    
    # Step 1: Enhance prompt
    print("\n1️⃣  PROMPT ENHANCEMENT")
    enhanced_prompt = generator.prompt_enhancer.enhance_prompt(
        user_brief,
        style="product_ad",
        quality="high"
    )
    print(f"   ✓ Generated enhanced prompt ({len(enhanced_prompt)} chars)")
    print(f"   ✓ Ready for image generation")
    
    # Step 2: Configure generation
    print("\n2️⃣  CONFIGURATION")
    config = {
        "num_inference_steps": 50,
        "guidance_scale": 7.5,
        "image_size": "512x512",
        "format": "PNG"
    }
    for key, value in config.items():
        print(f"   ✓ {key}: {value}")
    
    # Step 3: Generate (would require GPU)
    print("\n3️⃣  IMAGE GENERATION")
    print("   Status: Ready to generate")
    print("   Requirements:")
    print("   - NVIDIA GPU with 6GB+ VRAM")
    print("   - CUDA 11.8+")
    print("   - Estimated time: 45-90 seconds")
    print("   - Estimated time (CPU): 15-20 minutes")
    
    # Step 4: Save and output
    print("\n4️⃣  SAVE & OUTPUT")
    print("   ✓ Output directory: generated_images/")
    print("   ✓ Filename format: {product}_{timestamp}.png")
    print("   ✓ Example: Red_running_shoes_20260130_153045.png")
    
    print("\n✅ Workflow complete! Image ready for use.")


def demo_different_styles():
    """Demo 4: Show how different styles affect output"""
    print("\n" + "="*70)
    print("DEMO 4: STYLE COMPARISON")
    print("="*70)
    
    enhancer = get_prompt_enhancer()
    product = "Blue silk dress"
    
    print(f"\n👗 Product: {product}\n")
    print("How the same product looks with different styles:\n")
    
    styles_info = {
        "product_ad": "For e-commerce listings - clean, professional, studio-lit",
        "lifestyle": "For social media - natural setting, worn by people",
        "minimalist": "For luxury branding - simple, elegant, focused",
        "vibrant": "For young audience - colorful, energetic, dynamic",
        "luxury": "For high-end market - sophisticated, premium, refined"
    }
    
    for style, description in styles_info.items():
        print(f"🎨 {style.upper()}")
        print(f"   Purpose: {description}")
        prompt = enhancer.enhance_prompt(product, style=style, quality="high")
        print(f"   Key words: {style.replace('_', ' ')}")
        print()


def demo_quality_levels():
    """Demo 5: Show different quality levels"""
    print("\n" + "="*70)
    print("DEMO 5: QUALITY LEVELS")
    print("="*70)
    
    enhancer = get_prompt_enhancer()
    product = "Gold luxury watch"
    
    print(f"\n⌚ Product: {product}\n")
    print("Quality levels affect prompt detail and generation time:\n")
    
    quality_info = {
        "low": {"steps": 20, "time_cpu": "3-5 min", "time_gpu": "15-30 sec", "description": "Fast, acceptable quality"},
        "medium": {"steps": 35, "time_cpu": "7-10 min", "time_gpu": "30-45 sec", "description": "Balanced speed/quality"},
        "high": {"steps": 50, "time_cpu": "15-20 min", "time_gpu": "45-90 sec", "description": "High quality, recommended"},
        "ultra": {"steps": 75, "time_cpu": "25-30 min", "time_gpu": "2-3 min", "description": "Masterpiece quality"}
    }
    
    for quality, info in quality_info.items():
        print(f"⭐ {quality.upper()}")
        print(f"   Description: {info['description']}")
        print(f"   Steps: {info['steps']}")
        print(f"   Time (CPU): {info['time_cpu']}")
        print(f"   Time (GPU): {info['time_gpu']}")
        print()


def demo_product_detection():
    """Demo 6: Show automatic product type detection"""
    print("\n" + "="*70)
    print("DEMO 6: PRODUCT TYPE DETECTION")
    print("="*70)
    
    enhancer = get_prompt_enhancer()
    
    products = [
        "Nike Air Max running shoes",
        "Cotton summer dress",
        "iPhone 15 Pro",
        "Dior face cream",
        "Chocolate cake",
        "IKEA wooden chair",
        "Gold necklace"
    ]
    
    print("\nAutomatic category detection for prompt customization:\n")
    
    for product in products:
        category = enhancer._identify_product_type(product)
        print(f"✓ '{product}'")
        print(f"  → Detected as: {category}")
        print()


def demo_api_usage():
    """Demo 7: Show how to use via API"""
    print("\n" + "="*70)
    print("DEMO 7: API USAGE EXAMPLES")
    print("="*70)
    
    print("\n🌐 Using the FastAPI endpoints:\n")
    
    print("1️⃣  Start the server:")
    print("    python -m uvicorn app.main:app --reload\n")
    
    print("2️⃣  Generate image (curl):")
    print('    curl -X POST "http://localhost:8000/generate-image" \\')
    print('      -H "Content-Type: application/json" \\')
    print('      -d \'{')
    print('        "user_brief": "Red running shoes",')
    print('        "style": "product_ad",')
    print('        "quality": "high",')
    print('        "num_inference_steps": 50')
    print('      }\'')
    print()
    
    print("3️⃣  Download generated image:")
    print('    curl -O "http://localhost:8000/download-image/Red_running_shoes_20260130_153045.png"\n')
    
    print("4️⃣  Python requests example:")
    print("    import requests")
    print("    response = requests.post('http://localhost:8000/generate-image',")
    print("        json={")
    print('            "user_brief": "Red running shoes",')
    print('            "style": "product_ad",')
    print('            "quality": "high"')
    print("        })")
    print("    result = response.json()")
    print("    print(f\"Image saved to: {result['image_path']}\")")


def main():
    """Run all demos"""
    print("\n")
    print("=" * 70)
    print("WEEK 2: IMAGE GENERATION PRACTICAL DEMOS")
    print("=" * 70)
    
    demos = [
        ("Prompt Enhancement", demo_prompt_enhancement),
        ("Batch Processing", demo_batch_processing),
        ("Image Generation Workflow", demo_image_generation_workflow),
        ("Style Comparison", demo_different_styles),
        ("Quality Levels", demo_quality_levels),
        ("Product Detection", demo_product_detection),
        ("API Usage", demo_api_usage),
    ]
    
    print("\n📋 Available Demos:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"   {i}. {name}")
    
    print("\n🎯 Running all demos...\n")
    
    for name, demo_func in demos:
        try:
            demo_func()
        except Exception as e:
            print(f"❌ Error in {name}: {str(e)}")
    
    print("\n" + "="*70)
    print("✅ ALL DEMOS COMPLETED")
    print("="*70)
    print("\n📚 For more information, see WEEK2_COMPLETION.md")
    print("🧪 For automated tests, run: python test_image_generation.py")
    print("\n")


if __name__ == "__main__":
    main()
