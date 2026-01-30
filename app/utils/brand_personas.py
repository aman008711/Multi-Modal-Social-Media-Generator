"""
Brand Personas for Marketing Caption Generation
"""

BRAND_PERSONAS = {
    "luxury_brand": {
        "name": "Luxury Lifestyle",
        "tone": "sophisticated, elegant, exclusive",
        "style": "professional, refined",
        "emoji_preference": "minimal, classy",
        "typical_audience": "high-net-worth individuals",
        "example_phrases": [
            "exquisite craftsmanship",
            "timeless elegance",
            "exclusive collection",
            "luxury redefined"
        ]
    },
    "tech_startup": {
        "name": "Tech Innovator",
        "tone": "innovative, energetic, modern",
        "style": "casual, trendy, tech-savvy",
        "emoji_preference": "tech-related, rocket, lightning",
        "typical_audience": "millennials, tech enthusiasts",
        "example_phrases": [
            "game-changing technology",
            "disruptive innovation",
            "next-gen solution",
            "future is here"
        ]
    },
    "wellness_brand": {
        "name": "Health & Wellness",
        "tone": "caring, motivating, supportive",
        "style": "friendly, approachable, positive",
        "emoji_preference": "nature, health, wellness",
        "typical_audience": "health-conscious individuals",
        "example_phrases": [
            "holistic wellness",
            "transform your life",
            "natural ingredients",
            "mindful living"
        ]
    },
    "fashion_brand": {
        "name": "Fashion Forward",
        "tone": "trendy, inspiring, bold",
        "style": "creative, vibrant, visual",
        "emoji_preference": "fashion, sparkles, style",
        "typical_audience": "fashion enthusiasts, Gen Z",
        "example_phrases": [
            "style statement",
            "fashion trend",
            "runway ready",
            "express yourself"
        ]
    },
    "eco_friendly": {
        "name": "Eco Conscious",
        "tone": "passionate, informative, inspiring",
        "style": "authentic, environmental, thoughtful",
        "emoji_preference": "earth, plants, green",
        "typical_audience": "environmentally conscious consumers",
        "example_phrases": [
            "sustainable living",
            "mother earth approved",
            "eco-friendly choice",
            "planet-positive impact"
        ]
    }
}

def get_persona(persona_key):
    """Get a specific brand persona by key"""
    return BRAND_PERSONAS.get(persona_key)

def get_all_personas():
    """Get all available personas"""
    return BRAND_PERSONAS

def list_personas():
    """List all available persona names"""
    return list(BRAND_PERSONAS.keys())
