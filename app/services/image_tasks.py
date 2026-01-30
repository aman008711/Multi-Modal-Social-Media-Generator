from app.celery_worker import celery_app
from app.services.image_generator import get_image_generator

@celery_app.task(name="app.services.image_tasks.generate_image_task")
def generate_image_task(data: dict):
    
    user_prompt = data.get("prompt")
    
    generator = get_image_generator()
    result = generator.generate_image(user_prompt)
    
    return result