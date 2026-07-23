from fastapi import Depends, HTTPException, status

from app.schema.task_schema import TaskSchemaResponse, TaskSchemaRequest, TaskSchemaUpdate, TaskSchemaFilter
from app.utils.jwt_helper import get_current_user_from_token
from app.repository.app_repository import DBRepository
from app.utils.db_dependency import get_db_repository
from app.model.task import Task
from app.policies.policy import authorize
from app.policies.task_policy import TaskPolicy


async def create_task_service(task: TaskSchemaRequest, user_id:int=Depends(get_current_user_from_token), repo: DBRepository = Depends(get_db_repository)) -> TaskSchemaResponse:
    task_policy = TaskPolicy(user_id)
    await authorize(task_policy.can_create())
    new_task = await repo.create_record(Task, {**task.model_dump(), "user_id": user_id})
    return new_task

async def get_all_tasks_by_user_id_service(filter: TaskSchemaFilter = None, user_id:int=Depends(get_current_user_from_token), repo:DBRepository=Depends(get_db_repository) )->TaskSchemaResponse:
    task_policy = TaskPolicy(user_id)
    await authorize(task_policy.can_read_all())
    tasks = await repo.get_tasks(user_id=user_id, filter=filter)
    return tasks

async def get_task_by_id_service(task_id:int, user_id:int=Depends(get_current_user_from_token), repo:DBRepository=Depends(get_db_repository) )->TaskSchemaResponse:
    task_policy = TaskPolicy(user_id)
    tasks = await repo.get_record_by_value(Task, Task.id, task_id)
    await authorize(task_policy.can_read(tasks)) 
    return tasks

async def update_task_service(task_id:int, updated_task:TaskSchemaUpdate, repo:DBRepository=Depends(get_db_repository), user_id:int=Depends(get_current_user_from_token),)->TaskSchemaResponse:
    task = await repo.get_record_by_value(Task, Task.id, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    task_policy = TaskPolicy(user_id)
    await authorize(task_policy.can_update(task))
    updated_task = await repo.update_record_by_id(updated_task, task)
    return updated_task

async def delete_task_service(task_id:int, user_id:int=Depends(get_current_user_from_token), repo:DBRepository=Depends(get_db_repository))->None:
    task = await repo.get_record_by_value(Task, Task.id, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    task_policy = TaskPolicy(user_id)
    await authorize(task_policy.can_delete(task))
    await repo.delete_record_by_id(task)
    return None

