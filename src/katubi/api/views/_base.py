from typing import Type

from rest_framework import request, response, serializers, views

from katubi.application import message_bus
from katubi.application.types import Command


class CommandView(views.APIView):
    """
    An API view to process commands.

    Subclasses should provide a serializer to validate input data and a method to build
    messages to be handled by the message bus.
    """

    Serializer: Type[serializers.Serializer]

    def get_commands(self, request: request.Request, data: dict) -> list[Command]:
        """
        Build the commands this view should process on the message queue.

        This should be implemented by subclasses
        """
        raise NotImplementedError

    def get_validated_data(self, request: request.Request) -> dict:
        """
        Use the serializer to deserialize and validate the input data.

        Return the validated data.
        """
        # Deserialize the data.
        serializer = self.Serializer(data=request.data)

        # Validate the data.
        serializer.is_valid(raise_exception=True)

        # Return the validated data.
        return serializer.validated_data

    def post(self, request: request.Request) -> response.Response:
        """
        Create and process the commands for this view.
        """
        # Validate the request data.
        data = self.get_validated_data(request)

        # Build the commands and handle them on the message bus.
        commands = self.get_commands(request, data)
        message_bus.handle(commands)

        return response.Response()
