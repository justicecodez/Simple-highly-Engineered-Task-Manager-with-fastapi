from model import Task

class TaskPolicy:
    def __init__(self, user_id: int):
        self.user_id = user_id

    def can_create(self) -> bool:
        # All authenticated users can create tasks
        return self.user_id is not None

    def can_read(self, task: Task) -> bool:
        # Users can read their own tasks or if they are an admin
        return task.user_id == self.user_id 

    def can_read_all(self) -> bool:
        # Any authenticated user can list tasks
        return self.user_id is not None

    def can_update(self, task: Task) -> bool:
        # Users can update their own tasks or if they are an admin
        return task.user_id == self.user_id 

    def can_delete(self, task: Task) -> bool:
        # Users can delete their own tasks or if they are an admin
        return task.user_id == self.user_id 