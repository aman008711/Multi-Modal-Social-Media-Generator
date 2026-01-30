"""
Caption Generation Service
"""

from app.utils.llm_loader import get_llm
from app.utils.brand_personas import get_persona

class CaptionGenerator:
    def __init__(self):
        self.llm = None
    
    def initialize(self):
        """Initialize the LLM for caption generation"""
        self.llm = get_llm()
    
    def generate_caption(self, product_description, persona_key, num_captions=1):
        """
        Generate marketing captions based on product description and brand persona
        
        Args:
            product_description: Description of the product
            persona_key: Key of the brand persona to use
            num_captions: Number of captions to generate
            
        Returns:
            List of generated captions
        """
        if self.llm is None:
            try:
                self.initialize()
            except Exception as e:
                return {"error": f"Model not available: {str(e)}"}
        
        persona = get_persona(persona_key)
        if not persona:
            return {"error": f"Unknown persona: {persona_key}"}
        
        captions = []
        
        for i in range(num_captions):
            # Craft the prompt based on persona and product description
            prompt = self._craft_prompt(product_description, persona)
            
            try:
                # Generate caption
                caption = self.llm.generate_text(
                    prompt,
                    max_length=150,
                    temperature=0.8,
                    top_p=0.9
                )
                
                if caption:
                    # Extract just the caption part (remove the prompt)
                    caption_text = caption.replace(prompt, "").strip()
                    captions.append(caption_text)
            except Exception as e:
                print(f"Error generating caption: {e}")
                captions.append(f"[Generated using {persona_key} persona] Demo caption based on {product_description[:50]}...")
        
        return captions
    
    def _craft_prompt(self, product_description, persona):
        """Craft a prompt for caption generation"""
        tone = persona.get("tone", "")
        style = persona.get("style", "")
        
        prompt = f"""You are a {persona['name']} brand. Your tone is {tone}.
Your writing style is {style}.

Product: {product_description}

Generate a compelling marketing caption for social media:"""
        
        return prompt
    
    def generate_multi_persona_captions(self, product_description, personas_list=None):
        """
        Generate captions for multiple personas
        
        Args:
            product_description: Description of the product
            personas_list: List of persona keys (if None, use all personas)
            
        Returns:
            Dictionary with personas as keys and lists of captions as values
        """
        if personas_list is None:
            from app.utils.brand_personas import list_personas
            personas_list = list_personas()
        
        result = {}
        for persona_key in personas_list:
            captions = self.generate_caption(product_description, persona_key, num_captions=2)
            result[persona_key] = captions
        
        return result


# Create a global instance
caption_generator = CaptionGenerator()

def initialize_caption_generator():
    """Initialize the caption generator"""
    caption_generator.initialize()

def get_caption_generator():
    """Get the caption generator instance"""
    return caption_generator
