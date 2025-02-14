from asyncio import sleep
from typing import Any

from taskiq import TaskiqMessage, TaskiqMiddleware, TaskiqResult


class MyMiddleware(TaskiqMiddleware):
    async def pre_execute(self, message: "TaskiqMessage") -> TaskiqMessage:
        await sleep(1)
        return message

    async def post_save(
        self,
        message: "TaskiqMessage",
        result: "TaskiqResult[Any]",
    ) -> None:
        await sleep(1)
        print("Post save")
