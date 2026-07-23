from fastapi import Depends, HTTPException, status,APIRouter
from fastapi_limiter.depends import RateLimiter

from app.schema.task_schema import TaskSchemaRequest,TaskSchemaResponse,TaskSchemaFilter
from app.service.task_service import create_task_service, get_all_tasks_by_user_id_service, update_task_service
from app.utils.limiter import create_rate_limiter

router=APIRouter()

@router.post('/task', response_model=TaskSchemaResponse, dependencies=[Depends(create_rate_limiter(30, 60))])
async def create_task(task: TaskSchemaRequest, service: int = Depends(create_task_service)) -> TaskSchemaResponse:
    return service

@router.get('/tasks', response_model=TaskSchemaResponse, dependencies=[Depends(create_rate_limiter(30, 60))])
async def get_task_by_user_id(filter: TaskSchemaFilter = None, service: int = Depends(get_all_tasks_by_user_id_service)) -> TaskSchemaResponse:
    return service

@router.patch('/task/{task_id}', response_model=TaskSchemaResponse, dependencies=[Depends(create_rate_limiter(30, 60))])
async def update_task(task_id:int, task:TaskSchemaRequest, service:int=Depends(update_task_service))->TaskSchemaResponse:
    return service

@router.delete('/task/{task_id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(create_rate_limiter(30, 60))])
async def delete_task(task_id:int, service:int=Depends(update_task_service)):
    return service
