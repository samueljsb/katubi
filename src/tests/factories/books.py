import factory

from katubi.books import models


class Author(factory.django.DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = models.Author


class Book(factory.django.DjangoModelFactory):
    title = factory.Faker("sentence", nb_words=4)
    subtitle = factory.Faker("sentence", nb_words=6)
    description = factory.Faker("sentence", nb_words=20)

    class Meta:
        model = models.Book

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of authors was passed in; use them.
            for author in extracted:
                self.authors.add(author)
