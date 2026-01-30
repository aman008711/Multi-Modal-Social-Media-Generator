# WEEK 3: Async Processing with Celery – Background Image Generation

**Date:** January 30, 2026  
**Status:** ✅ COMPLETED 

---
## Executive Summary

In Week 3, asynchronous image generation was implemented using Celery and Redis. The image generation process was moved to a background worker to prevent API blocking. The system now returns a Job ID immediately after request submission. Users can check task status and retrieve results using the result endpoint. All test cases were successfully executed, confirming proper background processing and job tracking functionality.

## Week 3 Goal

To implement asynchronous image generation using Celery so that image processing runs in the background without blocking the FastAPI server.

Instead of waiting for the image to generate, the API should:
- Immediately return a Job ID
- Allow users to check status using a result endpoint

---

## Problem Statement

Image generation is a heavy task that takes several seconds to complete.
If executed directly inside the API:

- The API becomes slow
- The request blocks until completion
- Poor user experience
- Not scalable

To solve this, background task processing was implemented.

---

## Technologies Used

- FastAPI
- Celery
- Redis (Message Broker + Result Backend)
- Python

---

## Architecture Overview

Client  
   ↓  
POST /generate-image  
   ↓  
FastAPI  
   ↓  
Celery Task (Background Worker)  
   ↓  
Image Generation  
   ↓  
Store Result in Redis  
   ↓  
GET /result/{job_id}  

---

## Implementation Steps

### Step 1: Installed Dependencies

pip install celery redis

---

### Step 2: Configured Celery Worker

Created celery_worker.py:
- Configured Redis as broker
- Configured Redis as result backend
- Defined task routing

---

### Step 3: Created Background Task

Created image_tasks.py:
- Wrapped image generation inside Celery task
- Task returns:
  - status
  - image path

---

### Step 4: Updated FastAPI Endpoints

Added:

1️⃣ POST /generate-image  
- Starts background task  
- Returns job_id  

2️⃣ GET /result/{job_id}  
- Checks task status  
- Returns:
   - Processing
   - Completed result

---

## Testing Results

### ✅ Test Case 1:
Request:
POST /generate-image
Prompt: "Red Running Shoes"

Response:
{
  "message": "Image generation started",
  "job_id": "abc123"
}

---

###  ✅ Test Case 2:
GET /result/abc123

Response (after processing):
{
  "status": "completed",
  "image_path": "generated_images/xyz.png"
}

---

## Project Structure - Week 3 Updates

```

Multi-Modal-Social-Media-Generator/
│
├── app/
│   ├── __init__.py
│   ├── main.py                        # ✨ Updated with async endpoints
│   │
│   ├── celery_worker.py               # ✨ NEW - Week 3
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── caption_generator.py       # Week 1
│   │   ├── image_generator.py         # Week 2
│   │   ├── image_tasks.py             # ✨ NEW - Week 3 (Celery task)
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── brand_personas.py          # Week 1
│   │   ├── llm_loader.py              # Week 1
│   │   ├── prompt_enhancer.py         # Week 2
│
├── generated_images/                  # Week 2 - Output directory
│
├── test_caption_generation.py         # Week 1
├── test_image_generation.py           # Week 2
│
├── requirements.txt                   # ✨ Updated (Celery + Redis added)
├── README.md                          # ✨ Updated
├── WEEK1_COMPLETION.md                # Week 1
├── WEEK2_COMPLETION.md                # Week 2
├── WEEK3_COMPLETION.md                # ✨ NEW - Week 3


## ✅ Outcomes Achieved

- Successfully implemented asynchronous task processing
- Prevented API blocking during heavy operations
- Implemented job tracking system
- Improved scalability of image generation system
- Built production-style architecture

---

## 🎯 Key Learnings

- Understanding of asynchronous processing
- Working with message brokers (Redis)
- Background worker architecture
- Task lifecycle management in Celery
- API design for long-running tasks

---

## 📈 System Improvement

Before Week 3:
- Image generation was synchronous
- API waited until task completion

After Week 3:
- Image generation runs in background
- Immediate API response
- Scalable and efficient architecture

---

## 🔥 Conclusion

Week 3 successfully introduced asynchronous processing using Celery and Redis, making the Multi-Modal Social Media Generator more scalable and production-ready.

The system now supports:
✔ Text generation  
✔ Image generation  
✔ Background processing with Job ID tracking  

The project has moved closer to a real-world AI production system.