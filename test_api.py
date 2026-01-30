"""
Quick test script for the API
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api():
    print("\n" + "="*60)
    print("TESTING MARKETING CAPTION GENERATOR API")
    print("="*60 + "\n")
    
    # Test 1: Health check
    print("1️⃣  Testing Health Check...")
    try:
        resp = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"   ✅ Status: {resp.status_code}")
        print(f"   Response: {resp.json()}\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    # Test 2: Get available personas
    print("2️⃣  Testing Available Personas...")
    try:
        resp = requests.get(f"{BASE_URL}/personas", timeout=5)
        print(f"   ✅ Status: {resp.status_code}")
        data = resp.json()
        print(f"   Available Personas: {data['personas']}")
        print(f"   Count: {data['count']}\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    # Test 3: Generate caption for single persona
    print("3️⃣  Testing Single Persona Caption Generation...")
    product = "Premium wireless noise-canceling headphones with 30-hour battery"
    payload = {
        "product_description": product,
        "persona_key": "tech_startup",
        "num_captions": 1
    }
    
    try:
        resp = requests.post(f"{BASE_URL}/generate-caption", json=payload, timeout=30)
        print(f"   ✅ Status: {resp.status_code}")
        data = resp.json()
        print(f"   Product: {data['product_description']}")
        print(f"   Persona: {data['persona_key']}")
        print(f"   Captions:")
        for i, caption in enumerate(data['captions'], 1):
            print(f"      {i}. {caption}\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    # Test 4: Generate multi-persona captions
    print("4️⃣  Testing Multi-Persona Caption Generation...")
    payload = {
        "product_description": "Eco-friendly bamboo water bottle",
        "personas": ["eco_friendly", "wellness_brand"],
        "num_captions_per_persona": 1
    }
    
    try:
        resp = requests.post(f"{BASE_URL}/generate-multi-persona", json=payload, timeout=30)
        print(f"   ✅ Status: {resp.status_code}")
        data = resp.json()
        print(f"   Product: {data['product_description']}")
        print(f"   Results by Persona:")
        for persona, captions in data['results'].items():
            print(f"      {persona}:")
            for caption in captions:
                print(f"         - {caption}\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    print("="*60)
    print("✨ API TESTING COMPLETE")
    print("="*60)
    print("\n📖 Interactive API Documentation:")
    print("   http://localhost:8000/docs\n")

if __name__ == "__main__":
    time.sleep(2)  # Give server time to start
    test_api()
