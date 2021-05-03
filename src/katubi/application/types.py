from typing import Protocol, TypeVar, Union

from . import commands, events

Message = Union[commands.Command, events.Event]
M = TypeVar("M", commands.Command, events.Event, contravariant=True)


class Handler(Protocol[M]):
    def __call__(self, __message: M, __queue: list[Message]) -> None:
        ...
