import enum
from typing import Generic, Optional, Union

from pydantic.generics import GenericModel
from taskiq_dependencies import Depends
from typing_extensions import TypeVar

from taskiq.context import Context

_ProgressType = TypeVar("_ProgressType")


class TaskState(str, enum.Enum):
    """State of task execution."""

    STARTED = "STARTED"
    FAILURE = "FAILURE"
    SUCCESS = "SUCCESS"
    RETRY = "RETRY"


class TaskProgress(GenericModel, Generic[_ProgressType]):
    """Progress of task execution."""

    state: Union[TaskState, str]
    meta: _ProgressType


class ProgressTracker(Generic[_ProgressType]):
    """Task's dependency to set progress."""

    def __init__(
        self,
        context: Context = Depends(),
    ) -> None:
        self.context = context

    async def set_progress(
        self,
        state: Union[TaskState, str],
        meta: Optional[_ProgressType] = None,
    ) -> None:
        """Set progress.

        :param state: TaskState or str
        :param meta: progress data
        """
        if meta is None:
            progress = await self.get_progress()
            meta = progress.meta if progress else meta

        progress = TaskProgress(
            state=state,
            meta=meta,
        )

        await self.context.broker.result_backend.set_progress(
            self.context.message.task_id,
            progress,
        )

    async def get_progress(self) -> Optional[TaskProgress[_ProgressType]]:
        """Get progress."""
        return await self.context.broker.result_backend.get_progress(
            self.context.message.task_id,
        )
