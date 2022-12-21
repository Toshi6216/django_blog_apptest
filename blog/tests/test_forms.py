import datetime
from django.test import TestCase, Client
from .test_models import LoggedInTestCase
from django.urls import reverse, resolve, reverse_lazy
from .test_models import LoggedInTestCase
from blog.models import Post, Category, Profile, ContentCard
from django.contrib.auth import get_user_model
from PIL import Image
from ..forms import PostForm, ContentCardForm, CardFormset, CategoryForm
from django.utils import timezone


class PostFormTest(LoggedInTestCase):
    #python manage.py test blog.tests.test_forms.PostFormTest
    def test_post_form(self):
        form_data={
        #    "author": self.user,
            "category": 1,
            "title": "post form test",
        #    "created": timezone.now() - datetime.timedelta(days=30),
        #    "updated": timezone.now(),
        }
        form = PostForm(data=form_data)
        #print(form)
        self.assertTrue(form.is_valid())

    def test_contentdardform(self):
        self.category = Category.objects.create(
            name='test_category2',
        )
        
        category_obj = self.category
        self.post = Post.objects.create(
            author = self.user,
            category = category_obj,
            title = 'test_title2',
            created = timezone.now() - datetime.timedelta(days=30),
            updated = timezone.now() - datetime.timedelta(days=10),

        )
        #self.post.save()
        #post_obj = self.post
        post_data = Post.objects.all()
        print(f"post_data_count: {post_data.count()}")
        contentcardform_data={
            #"category": 1,
            "post":2,
            #"contentcard-0-content": "post_formset_content_test",
            "content": "contentcard_form_content_test"
        
        }
        form = ContentCardForm(data=contentcardform_data)
        print("ContentCardForm:")
        print(form)
        self.assertTrue(form.is_valid)

    def test_formset(self):
        formset_data={
            "category": 1,
            "title": "post form test",
            "post":1,
            "contentcard-0-content": "post_formset_content_test<p>ttt</p>",
        
        }
        #form =CardFormset(data=formset_data)
        cardformset =CardFormset(formset_data)
        print("cardformset.is_valid:")
        print(cardformset.is_valid)
        self.assertTrue(cardformset.is_valid)