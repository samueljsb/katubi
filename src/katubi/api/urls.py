from django.urls import path

from . import views

urlpatterns = [
    path("record-reading-started/", views.RecordReadingStartedFromISBN.as_view()),
    path("record-reading-finished/", views.RecordReadingFinishedFromISBN.as_view()),
]
