import datetime
from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import Faker, post_generation
from django.utils import timezone
from django.template.defaultfilters import slugify
import factory.fuzzy

from apps.blog.models import Author, Blog, Entry, Comment


class UserFactory(factory.django.DjangoModelFactory):

    username = Faker("user_name")
    email = Faker("email")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (extracted if extracted else Faker("password", length=42, special_chars=True, digits=True, upper_case=True, lower_case=True,).generate(extra_kwargs={}))
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]
        

class AuthorFactory(factory.django.DjangoModelFactory):
    name = Faker("name")
    email = Faker("email")

    class Meta:
        model = Author


class BlogFactory(factory.django.DjangoModelFactory):
    name = Faker('sentence', nb_words=4)
    tagline = Faker('sentence', nb_words=6)

    class Meta:
        model = Blog


class EntryFactory(factory.django.DjangoModelFactory):
    blog = factory.SubFactory(BlogFactory)
    headline = Faker('sentence', nb_words=6)
    body_text = Faker('text')
    pub_date = factory.fuzzy.FuzzyDate(datetime.date(2019, 1, 1))
    mod_date = factory.fuzzy.FuzzyDate(datetime.date.today())
    n_comments = factory.fuzzy.FuzzyInteger(10, 20)
    n_pingbacks = factory.fuzzy.FuzzyInteger(5, 10)
    rating = factory.fuzzy.FuzzyInteger(1, 5)

    class Meta:
        model = Entry

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for author in extracted:
                self.authors.add(author)


class CommentFactory(factory.django.DjangoModelFactory):
    entry = factory.SubFactory(EntryFactory)
    text = Faker('text')
    likes = factory.fuzzy.FuzzyInteger(10, 20)

    class Meta:
        model = Comment


# class CheeseFactory(factory.django.DjangoModelFactory):
#     name = factory.fuzzy.FuzzyText()
#     slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
#     description = factory.Faker('paragraph', nb_sentences=3, variable_nb_sentences=True)
#     firmness = factory.fuzzy.FuzzyChoice([x[0] for x in Cheese.Firmness.choices])
#     country_of_origin = factory.Faker('country_code')
#     creator = factory.SubFactory(UserFactory)
#
#     class Meta:
#         model = Cheese