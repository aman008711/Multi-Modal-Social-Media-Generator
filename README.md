# Marketing Caption Generator

Generate compelling marketing captions using the Phi-2 open-source LLM with brand-specific personas.

## Project Structure

```
Multi-Modal-Social-Media-Generator/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── celery_worker.py 
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├──caption_generator.py # Caption generation service
│   │   └── image_tasks.py  
│   └── utils/
│       ├── __init__.py
│       ├── brand_personas.py    # Brand persona definitions
│       └── llm_loader.py        # Phi-2 model loader
├── test_caption_generation.py  # Test suite
└── README.md
```

## Installation

### Prerequisites
- Python 3.8+
- CUDA (optional, for GPU acceleration)

### Setup

1. **Create virtual environment** (if not already done):
```bash
python -m venv .venv
.venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install transformers torch fastapi uvicorn celery redis
```

## Usage

### 1. Test the System

Run the comprehensive test suite:
```bash
python test_caption_generation.py
```

This will:
- Verify brand personas are loaded
- Initialize the Phi-2 LLM
- Generate sample marketing captions
- Show available API endpoints

### 2. Start Redis
redis-server
# OR
docker run -p 6379:6379 redis

### 3. Start Celery Worker
celery -A app.celery_worker.celery_app worker --loglevel=info

### 4. Start the FastAPI Server

```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

### 5. API Endpoints

#### Get Available Personas
```bash
curl http://localhost:8000/personas
```

#### Generate Single Persona Caption
```bash
curl -X POST http://localhost:8000/generate-caption \
  -H "Content-Type: application/json" \
  -d '{
    "product_description": "Premium noise-canceling wireless headphones",
    "persona_key": "tech_startup",
    "num_captions": 1
  }'
```

#### Generate Multi-Persona Captions
```bash
curl -X POST http://localhost:8000/generate-multi-persona \
  -H "Content-Type: application/json" \
  -d '{
    "product_description": "Eco-friendly bamboo water bottle",
    "personas": ["eco_friendly", "wellness_brand"],
    "num_captions_per_persona": 2
  }'
```

### 6. Interactive API Documentation

Visit `http://localhost:8000/docs` in your browser for Swagger UI documentation.

## Available Brand Personas

1. **luxury_brand** - Sophisticated, elegant, exclusive tone
2. **tech_startup** - Innovative, energetic, modern style
3. **wellness_brand** - Caring, motivating, supportive approach
4. **fashion_brand** - Trendy, inspiring, bold messaging
5. **eco_friendly** - Passionate, informative, environmental focus

## Key Features

✅ **Open Source LLM**: Uses Phi-2 (Microsoft's efficient language model)
✅ **Brand Personas**: Generate captions tailored to specific brand voices
✅ **FastAPI**: RESTful API with automatic documentation
✅ **Flexible Output**: Single or multiple captions, single or multiple personas
✅ **GPU Support**: Automatic CUDA detection for faster generation

## Example Output

**Product**: Premium wireless headphones

**Tech Startup Persona**:
- "Experience the future of audio with our revolutionary noise-canceling headphones—game-changing technology meets sleek design."

**Luxury Brand Persona**:
- "Indulge in exquisite craftsmanship with our premium headphones collection, a timeless symbol of audio excellence."

**Wellness Brand Persona**:
- "Transform your listening experience with our wellness-focused headphones, designed for mindful audio enjoyment."

## Configuration

### Modify LLM Settings
Edit `app/utils/llm_loader.py` to adjust:
- Model precision (float16, float32)
- Device assignment
- Generation parameters

### Add New Personas
Edit `app/utils/brand_personas.py` to add new brand voices with:
- Tone and style descriptions
- Target audience
- Example phrases

## Performance Notes

- First run downloads the Phi-2 model (~6GB)
- Subsequent runs load from cache
- GPU acceleration recommended for faster generation
- CPU mode available for testing

## Troubleshooting

### Out of Memory
Reduce `max_length` parameter in caption generation or use CPU mode on smaller systems.

### Slow Model Loading
Download happens on first run. Subsequent requests are faster.

### GPU Not Detected
Ensure PyTorch CUDA is properly installed. The system will automatically fallback to CPU.

---

## 🚀 Week 3 – Async Image Processing

### Overview
Image generation now runs as a background task using Celery and Redis.

### What Changed?
- Integrated Celery for async task handling
- Configured Redis as broker and backend
- API now returns Job ID immediately
- Added result endpoint for status tracking

### Benefits
- Non-blocking API
- Improved scalability
- Production-ready architecture

## Next Steps

- [ ] Add image analysis for visual content
- [ ] Implement hashtag generation
- [ ] Create caption templates
- [ ] Add A/B testing for captions
- [ ] Build web dashboard

---

**Version**: 1.3.0
**Created**: Week 1 Development Cycle
**Status**: Testing Phase ✅
 

---

''' 
Workflow 1: Quick Test
python test_api.py

Workflow 2: Run Full Server (Async Mode -Week 3)

1️⃣ Start Redis
redis-server
OR
docker run -p 6379:6379 redis

2️⃣ Start Celery Worker
celery -A app.celery_worker.celery_app worker --loglevel=info

3️⃣ Start FastAPI Server
uvicorn app.main:app --host localhost --port 8000
# Open http://localhost:8000/docs in browser

Workflow 3: Development
python -m uvicorn app.main:app --reload --host localhost --port 8000
'''