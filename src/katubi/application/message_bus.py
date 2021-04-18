import logging
from typing import Dict, Iterable, Iterator, Protocol, Type, TypeVar

from katubi.domain import messages

M = TypeVar("M", bound=messages.Message, contravariant=True)


class Handler(Protocol[M]):
    def __call__(self, __message: M) -> Iterable[messages.Event]:
        ...


# Event handlers.
# Each event type can be handled by multiple handlers.
EVENT_HANDLERS: Dict[Type[messages.Event], Iterable[Handler[messages.Event]]] = {}

# Command handlers.
# Each command type is handled by a single handler.
COMMAND_HANDLERS: Dict[Type[messages.Event], Handler[messages.Command]] = {}


# Handling messages.


def handle(
    message: messages.Message,
    *,
    event_handlers=EVENT_HANDLERS,
    command_handlers=COMMAND_HANDLERS,
) -> None:
    """
    Handle a message.

    Recursively handle any new messages generated as a result of this action.
    """
    message_queue = [message]
    while message_queue:
        # Get the message at the front of the queue
        next_message = message_queue.pop(0)

        # Handle the message and add any new messages to the end of the queue.
        new_messages: Iterable[messages.Message]
        if isinstance(next_message, messages.Event):
            new_messages = _handle_event(next_message, event_handlers)
        elif isinstance(next_message, messages.Command):
            new_messages = _handle_command(next_message, command_handlers)
        else:
            raise TypeError(next_message)
        message_queue.extend(new_messages)


def _handle_event(event: messages.Event, handler_map) -> Iterator[messages.Event]:
    """
    Handle an event.

    Yields any new events that are created by the handling of this one.
    """
    # Get the handlers for this event type.
    try:
        handlers = handler_map[type(event)]
    except KeyError:
        logging.exception("no handlers found for event %s", event)
        raise TypeError(event)

    # Handle the event with each handler, yielding any new events that are generated.
    for handler in handlers:
        try:
            logging.debug("handling event %s with handler %s", event, handler)
            yield from handler(event)
        except Exception as exc:
            logging.exception("Exception handling event %s", event, exc_info=exc)
            continue


def _handle_command(command: messages.Command, handler_map) -> Iterable[messages.Event]:
    """
    Process a command.

    Returns any events that were created as a result of this command.
    """
    # Get the handler for this command type.
    try:
        handler = handler_map[type(command)]
    except KeyError:
        logging.exception("no handler found for command %s", command)
        raise TypeError(command)

    # Handle the comand and return any new events that are generated.
    try:
        logging.debug("handling command %s with handler %s", command, handler)
        return handler(command)
    except Exception as exc:
        logging.exception("Exception handling command %s", command, exc_info=exc)
        raise
