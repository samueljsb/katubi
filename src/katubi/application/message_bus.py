from typing import Union

from . import commands, events

Message = Union[commands.Command, events.Event]


def handle(message_queue: list[Message]) -> None:
    raise NotImplementedError
