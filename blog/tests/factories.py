import datetime
import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from ..models import Post, ContentCard, Category

from factory import LazyAttribute, Sequence
from factory.django import DjangoModelFactory, ImageField
from factory.fuzzy import FuzzyDateTime
from factory import Faker, RelatedFactory


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
    
    auther = get_user_model().objects.filter(username='test_user')
    category = Category.objects.filter(name='test_category')
    title = Faker('word', local=FAKER_LOCAL)
    created = timezone.now() - datetime.timedelta(days=40)
    updated = timezone.now() - datetime.timedelta(days=20)

    relatedparent = RelatedFactory(
        ContentCardFactory, 'post'
    )