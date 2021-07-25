import factory

from katubi.volumes import lookup, models

from . import books


class VolumeInfo(factory.Factory):
    class Meta:
        model = lookup.VolumeInfo

    title = factory.Faker("sentence", nb_words=4)
    subtitle = factory.Faker("sentence", nb_words=6)
    description = factory.Faker("sentence", nb_words=20)
    authors = factory.List([factory.Faker("name"), factory.Faker("name")])
    image_url = factory.Faker("image_url")


class Volume(factory.django.DjangoModelFactory):
    book = factory.SubFactory(books.Book)
    isbn = factory.Faker("isbn13", separator="")
    cover_image_url = factory.Faker("image_url")

    class Meta:
        model = models.Volume
