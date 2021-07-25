import factory

from katubi.volumes import models

from . import books


class Volume(factory.django.DjangoModelFactory):
    book = factory.SubFactory(books.Book)
    isbn = factory.Faker("isbn13", separator="")
    cover_image_url = factory.Faker("image_url")

    class Meta:
        model = models.Volume
