from rest_framework import generics, request, response, serializers, status

from katubi.application import reading_events


class RecordReadingEventFromISBNSerializer(serializers.Serializer):
    isbn = serializers.CharField(max_length=13)
    date = serializers.DateField()


class RecordReadingStartedFromISBN(generics.GenericAPIView):
    """
    View to record a reading started event.

    The book that is being read is determined from the isbn.
    """

    serializer_class = RecordReadingEventFromISBNSerializer

    def post(self, request: request.Request) -> response.Response:
        # Validate the data.
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return response.Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializer.errors
            )

        # Record the reading event.
        try:
            reading_events.record_reading_started_from_isbn(
                isbn=serializer.validated_data["isbn"],
                date=serializer.validated_data["date"],
                user=request.user,
            )
        except reading_events.CannotRecordReadingEvent:
            return response.Response(status=status.HTTP_404_NOT_FOUND)

        return response.Response(status=status.HTTP_200_OK)


class RecordReadingFinishedFromISBN(generics.GenericAPIView):
    """
    View to record a reading finished event.

    The book that is being read is determined from the isbn.
    """

    serializer_class = RecordReadingEventFromISBNSerializer

    def post(self, request: request.Request) -> response.Response:
        # Validate the data.
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return response.Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializer.errors
            )

        # Record the reading event.
        try:
            reading_events.record_reading_finished_from_isbn(
                isbn=serializer.validated_data["isbn"],
                date=serializer.validated_data["date"],
                user=request.user,
            )
        except reading_events.CannotRecordReadingEvent:
            return response.Response(status=status.HTTP_404_NOT_FOUND)

        return response.Response(status=status.HTTP_200_OK)
