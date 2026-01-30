"""
LLM Loader for Language Models (distilgpt2 by default for faster startup)
For production, you can swap to microsoft/phi-2 or other larger models
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class Phi2Loader:
    def __init__(self, model_name="distilgpt2"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None
        
    def load_model(self):
        """Load the LLM model and tokenizer"""
        try:
            print(f"Loading model {self.model_name} on device: {self.device}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map=self.device,
                trust_remote_code=True
            )
            
            print("Model loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def generate_text(self, prompt, max_length=100, temperature=0.7, top_p=0.9):
        """Generate text based on the given prompt"""
        if self.model is None or self.tokenizer is None:
            raise Exception("Model not loaded. Call load_model() first.")
        
        try:
            # Encode the prompt
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            # Generate text
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode the output
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return generated_text
        except Exception as e:
            print(f"Error generating text: {e}")
            return None
    
    def unload_model(self):
        """Unload the model to free memory"""
        self.model = None
        self.tokenizer = None
        torch.cuda.empty_cache()
        print("Model unloaded and memory cleared.")


# Create a global instance for the application
phi2_loader = None

def initialize_llm():
    """Initialize the Phi-2 LLM"""
    global phi2_loader
    phi2_loader = Phi2Loader()
    phi2_loader.load_model()
    return phi2_loader

def get_llm():
    """Get the global LLM instance"""
    global phi2_loader
    if phi2_loader is None:
        initialize_llm()
    return phi2_loader
