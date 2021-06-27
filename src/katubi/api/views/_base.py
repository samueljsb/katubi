from rest_framework import generics, request, response, status

from katubi.application import message_bus
from katubi.application.types import Command


class CommandView(generics.GenericAPIView):
    """
    An API view to process commands.

    Subclasses must provide a method to build messages to be handled by the message bus.
    """

    def post(self, request: request.Request) -> response.Response:
        """
        Create and process the commands for this view.
        """
        # Validate the data.
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return response.Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializer.errors
            )

        # Build the commands and handle them on the message bus.
        commands = self.get_commands(request)
        message_bus.handle(commands)

        return response.Response(status=status.HTTP_200_OK)

    def get_commands(self, request: request.Request) -> list[Command]:
        """
        Build the commands this view should process on the message queue.

        This must be implemented by subclasses.
        """
        raise NotImplementedError

    def _validate_data(self, request: request.Request) -> dict:
        """
        Check the parsed data exists and is in a valid form.

        Returns a dict of serializer errors, if there are any.
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors
        return {}
