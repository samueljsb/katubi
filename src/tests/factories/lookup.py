import factory

from katubi import lookup


class BookInfo(factory.Factory):
    class Meta:
        model = lookup.BookInfo

    title = factory.Faker("sentence", nb_words=4)
    subtitle = factory.Faker("sentence", nb_words=6)
    description = factory.Faker("sentence", nb_words=20)
    authors = factory.List([factory.Faker("name"), factory.Faker("name")])
    image_url = factory.Faker("image_url")
