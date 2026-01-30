"""
Prompt Enhancer for converting user briefs to enhanced prompts for image generation
"""

class PromptEnhancer:
    """Enhance user briefs into detailed, high-quality image generation prompts"""
    
    def __init__(self):
        self.style_keywords = {
            "product_ad": "professional product photography, studio lighting, white background, high quality, detailed",
            "lifestyle": "lifestyle photography, natural lighting, real people, authentic, lifestyle context",
            "minimalist": "minimalist design, clean background, simple, elegant, focused product",
            "vibrant": "vibrant colors, energetic, dynamic, colorful, bright lighting",
            "luxury": "luxury, premium, sophisticated, high-end, elegant, refined"
        }
        
        self.product_contexts = {
            "shoes": "professional product shot, detailed footwear, showcasing design and texture",
            "apparel": "clothing displayed on model or hanger, showing fit and fabric detail",
            "electronics": "tech product, sleek design, modern, showing all features",
            "beauty": "cosmetic product, luxurious presentation, sophisticated lighting",
            "food": "appetizing food presentation, professional food photography",
            "furniture": "interior design context, room setting, modern aesthetic",
            "accessories": "jewelry or accessory display, elegant presentation"
        }
    
    def enhance_prompt(self, user_brief: str, style: str = "product_ad", quality: str = "high") -> str:
        """
        Convert a simple user brief into an enhanced, detailed prompt for image generation
        
        Args:
            user_brief: Simple user description (e.g., "Red running shoes")
            style: Style of the image (product_ad, lifestyle, minimalist, vibrant, luxury)
            quality: Quality level (low, medium, high, ultra)
            
        Returns:
            Enhanced prompt string for image generation
        """
        
        # Determine product type for context
        product_type = self._identify_product_type(user_brief)
        
        # Get style modifiers
        style_mods = self.style_keywords.get(style, self.style_keywords["product_ad"])
        
        # Get product context
        context = self.product_contexts.get(product_type, "professional product photography")
        
        # Quality modifiers
        quality_map = {
            "low": "standard quality",
            "medium": "high quality, detailed",
            "high": "ultra high quality, professional photography, intricate details",
            "ultra": "4K ultra high definition, professional studio photography, masterpiece quality, intricate details, perfect lighting"
        }
        quality_mod = quality_map.get(quality, quality_map["high"])
        
        # Build enhanced prompt
        enhanced_prompt = f"""
A {quality_mod} image of {user_brief}.
{context}.
{style_mods}.
Professional lighting, perfect composition, well-balanced exposure.
Product photography style, commercial quality.
""".strip()
        
        return enhanced_prompt
    
    def _identify_product_type(self, brief: str) -> str:
        """Identify product type from brief for better context"""
        brief_lower = brief.lower()
        
        for product_key, keywords in {
            "shoes": ["shoe", "shoes", "sneaker", "boot", "running", "athletic"],
            "apparel": ["shirt", "dress", "pants", "jacket", "hoodie", "sweater", "clothing"],
            "electronics": ["phone", "laptop", "headphone", "camera", "watch", "device"],
            "beauty": ["lipstick", "makeup", "perfume", "cream", "cosmetic"],
            "food": ["cake", "pizza", "burger", "food", "drink", "beverage"],
            "furniture": ["chair", "table", "sofa", "bed", "furniture"],
            "accessories": ["watch", "bag", "belt", "scarf", "jewelry", "necklace", "bracelet", "diamond"]
        }.items():
            if any(keyword in brief_lower for keyword in keywords):
                return product_key
        
        return "product"
    
    def batch_enhance(self, briefs: list, style: str = "product_ad", quality: str = "high") -> list:
        """
        Enhance multiple briefs at once
        
        Args:
            briefs: List of user briefs
            style: Style to apply to all
            quality: Quality level to apply to all
            
        Returns:
            List of enhanced prompts
        """
        return [self.enhance_prompt(brief, style, quality) for brief in briefs]


# Create a global instance
_prompt_enhancer = None

def get_prompt_enhancer() -> PromptEnhancer:
    """Get or create the prompt enhancer instance"""
    global _prompt_enhancer
    if _prompt_enhancer is None:
        _prompt_enhancer = PromptEnhancer()
    return _prompt_enhancer
