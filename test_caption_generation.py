"""
Test script for Marketing Caption Generator
Run this to test caption generation with different personas
"""

import sys
from app.utils.brand_personas import list_personas, get_persona
from app.utils.llm_loader import Phi2Loader
from app.services.caption_generator import CaptionGenerator

def test_brand_personas():
    """Test brand personas are loaded correctly"""
    print("=" * 60)
    print("TESTING BRAND PERSONAS")
    print("=" * 60)
    
    personas = list_personas()
    print(f"\nAvailable personas: {personas}\n")
    
    for persona_key in personas:
        persona = get_persona(persona_key)
        print(f"📊 {persona['name'].upper()}")
        print(f"   Tone: {persona['tone']}")
        print(f"   Style: {persona['style']}")
        print(f"   Audience: {persona['typical_audience']}")
        print()

def test_llm_loading():
    """Test LLM loader initialization"""
    print("=" * 60)
    print("TESTING LLM LOADER")
    print("=" * 60)
    
    try:
        print("\nInitializing Phi-2 Model (this may take a few minutes)...")
        loader = Phi2Loader()
        
        if loader.load_model():
            print("✅ Model loaded successfully!")
            print(f"   Model: {loader.model_name}")
            print(f"   Device: {loader.device}")
            return loader
        else:
            print("❌ Failed to load model")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_caption_generation(loader):
    """Test caption generation"""
    print("\n" + "=" * 60)
    print("TESTING CAPTION GENERATION")
    print("=" * 60)
    
    if loader is None:
        print("⚠️  Skipping caption generation test (no LLM loaded)")
        return
    
    # Test product
    product = "Premium noise-canceling wireless headphones with 30-hour battery life and superior sound quality"
    
    print(f"\n📱 Product: {product}\n")
    
    generator = CaptionGenerator()
    generator.llm = loader
    
    # Generate captions for different personas
    test_personas = ["luxury_brand", "tech_startup", "wellness_brand"]
    
    for persona_key in test_personas:
        if persona_key in list_personas():
            print(f"\n🎯 Generating caption for: {persona_key}")
            print("-" * 40)
            
            try:
                caption = generator.generate_caption(product, persona_key, num_captions=1)
                if caption:
                    for i, cap in enumerate(caption, 1):
                        print(f"Caption {i}: {cap}")
                else:
                    print("No caption generated")
            except Exception as e:
                print(f"Error: {e}")

def main():
    """Run all tests"""
    print("\n" + "🚀" * 30)
    print("MARKETING CAPTION GENERATOR - TEST SUITE")
    print("🚀" * 30 + "\n")
    
    # Test 1: Brand Personas
    test_brand_personas()
    
    # Test 2: LLM Loading
    loader = test_llm_loading()
    
    # Test 3: Caption Generation
    test_caption_generation(loader)
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    print("\n✨ To start the FastAPI server, run:")
    print("   uvicorn app.main:app --reload")
    print("\n📖 API Documentation will be available at:")
    print("   http://localhost:8000/docs")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⛔ Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
