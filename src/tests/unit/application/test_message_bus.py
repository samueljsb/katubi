import pytest

from katubi.application import message_bus
from katubi.domain import messages


class SomethingHappened(messages.Event):
    pass


class SomethingElseHappened(messages.Event):
    pass


class DoSomething(messages.Command):
    pass


class SomethingWentWrong(Exception):
    pass


class TestHandle:
    def test_happy_path(self):
        log = []
        command = DoSomething()

        def handle_do_something(command):
            log.append("do something")
            return [SomethingHappened(), SomethingElseHappened()]

        def handle_something_happened(event):
            log.append("something happened")
            return [SomethingElseHappened()]

        def handle_something_happened_again(event):
            log.append("something happened again")
            raise SomethingWentWrong

        def handle_something_else_happened(event):
            log.append("something else happened")
            return []

        message_bus.handle(
            command,
            event_handlers={
                SomethingHappened: [
                    handle_something_happened,
                    handle_something_happened_again,
                ],
                SomethingElseHappened: [handle_something_else_happened],
            },
            command_handlers={DoSomething: handle_do_something},
        )

        assert log == [
            "do something",
            "something happened",
            "something happened again",
            "something else happened",
            "something else happened",
        ]

    def test_raises_if_message_neither_event_not_command(self):
        message = messages.Message()

        with pytest.raises(TypeError):
            message_bus.handle(message)

    def test_raises_if_event_not_configured(self):
        event = SomethingHappened()

        with pytest.raises(TypeError):
            message_bus.handle(event, event_handlers={})

    def test_raises_if_command_not_configured(self):
        command = DoSomething()

        with pytest.raises(TypeError):
            message_bus.handle(command, command_handlers={})

    def test_ignores_failed_event(self):
        event = SomethingHappened()

        def handle_something_happened(event):
            raise SomethingWentWrong

        message_bus.handle(
            event, event_handlers={SomethingHappened: [handle_something_happened]}
        )

    def test_raises_if_command_fails(self):
        command = DoSomething()

        def handle_do_something(command):
            raise SomethingWentWrong

        with pytest.raises(SomethingWentWrong):
            message_bus.handle(
                command, command_handlers={DoSomething: handle_do_something}
            )
