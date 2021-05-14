from typing import Type

from . import commands, events, handlers
from .types import Handler, MessageQueue

EVENT_HANDLERS: dict[Type[events.Event], list[Handler]] = {}

COMMAND_HANDLERS: dict[Type[commands.Command], Handler] = {
    commands.RecordReadingStarted: handlers.record_reading_started,
    commands.RecordReadingFinished: handlers.record_reading_finished,
}


def handle(message_queue: MessageQueue) -> None:
    while message_queue:
        next_message = message_queue.pop(0)

        if isinstance(next_message, events.Event):
            _handle_event(next_message, message_queue)
        elif isinstance(next_message, commands.Command):
            _handle_command(next_message, message_queue)
        else:
            # This should never happen.
            raise TypeError("Message not recognised.")


def _handle_event(event: events.Event, message_queue: MessageQueue) -> None:
    """
    Handle the event with each of its configured handlers.

    If there are no handlers configured for this event type, do nothing.
    """
    handlers = EVENT_HANDLERS.get(type(event))

    if not handlers:
        # TODO: log this.
        return

    for handler in handlers:
        handler(event, message_queue)


def _handle_command(command: commands.Command, message_queue: MessageQueue) -> None:
    """
    Handle the command with its configured handlers.

    If no handler is configured for this command type, do nothing.
    """
    handler = COMMAND_HANDLERS.get(type(command))

    if handler:
        handler(command, message_queue)
    else:
        # TODO: log this.
        pass
