import datetime
import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from ..models import Post, ContentCard, Category

from factory import LazyAttribute, Sequence
from factory.django import DjangoModelFactory, ImageField
from factory.fuzzy import FuzzyDateTime
from factory import  RelatedFactory, SubFactory
from faker import Faker
import factory


tzinfo = pytz.timezone(settings.TIME_ZONE)
UserModel = get_user_model()

#FAKER_LOCAL = 'ja_JP'
fake=Faker('JA_jp')    


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post
    
    auther = get_user_model().objects.filter(username='test_user')
    #category = Category.objects.filter(name='test_category')
    title = 'test_title_fact'
    created = timezone.now() - datetime.timedelta(days=40)
    updated = timezone.now() - datetime.timedelta(days=20)

    
#class ContentCardFactory(DjangoModelFactory):
#    image = ImageField()
#    class Meta:
#        model = ContentCard
#    content = fake('text',max_nb_chars=100)
#    post = SubFactory(PostFactory, title='test_title_fact')
#
#class CategoryFactory(DjangoModelFactory):
#    class Meta:
#        model=Category
#    name = 'test_category_fact'
#    relatedparent = RelatedFactory(PostFactory, post)

   
