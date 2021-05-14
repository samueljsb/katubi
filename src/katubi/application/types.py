from typing import Protocol, TypeVar, Union

from .commands import Command
from .events import Event

MessageQueue = Union[list[Command], list[Event], list[Union[Command, Event]]]

M = TypeVar("M", Command, Event, contravariant=True)


class Handler(Protocol[M]):
    def __call__(self, __message: M, __queue: MessageQueue) -> None:
        ...
