from sqlalchemy import select
from database import TaskORM, new_session
from schemas import TaskAddSchema, TaskSchema


class TaskRepository:
    @classmethod
    async def add_one(cls, data: TaskAddSchema) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()

            task = TaskORM(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id


    @classmethod
    async def find_all(cls) -> list[TaskSchema]:
        async with new_session() as session:
            query = select(TaskORM)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [TaskSchema.model_validate(task_model) for task_model in task_models]
            return task_schemas