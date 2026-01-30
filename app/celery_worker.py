from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.task_routes = {
    "app.services.image_tasks.generate_image_task": {"queue": "image_queue"}
}

import app.services.image_tasks