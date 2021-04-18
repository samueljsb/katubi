"""
Base classes for objects handled by the message bus.
"""


class Message:
    pass


class Event(Message):
    pass


class Command(Message):
    pass
