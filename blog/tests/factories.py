import datetime
import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from ..models import Post, ContentCard

from factory import LazyAttribute, Sequence
from factory.django import DjangoModelFactory, ImageField
from factory.fuzzy import FuzzyDateTime
from factory import Faker
from .test_urls import LoggedInTestCase

tzinfo = pytz.timezone(settings.TIME_ZONE)
UserModel = get_user_model()

FAKER_LOCAL = 'ja_JP'

class ContentCardFactory(DjangoModelFactory):
    class Meta:
        model = ContentCard
    content = Faker('text',max_nb_chars=100, local=FAKER_LOCAL)
    image = ImageField()
    
class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post
    #auther = 
    #category
    #title = Faker('word', local=FAKER_LOCAL)
    #created
    #updated