from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from blog.models import Post, Category, Profile, ContentCard
from ..models import Category, Post
from django.utils import timezone
import datetime
from PIL import Image
from .factories import ContentCardFactory, PostFactory
import io

class LoggedInTestCase(TestCase):
    def setUp(self):
        #テストユーザー作成
        self.password='password'
        User = get_user_model()
        self.user = User.objects.create_user(
            username='test_user',
            email='test@aaa.ccc',
            password=self.password,
            
         )
        user_obj=self.user
        #user_obj.save()
        saved_user = User.objects.all()
        #ユーザーデータが１つできていることを確認
        self.assertEqual(saved_user.count(), 1)
        

        #作成したユーザーデータでログイン
        self.client=Client()
        self.client.login(
            username=user_obj.username,
            password=self.password,
        )

        #Profileデータ作成
        self.profile = Profile.objects.create(
            user = user_obj,
            nickname='test_nickname',
            )
        #self.profile.save()
        saved_nickname = user_obj.profile.nickname
        
        #ユーザーデータに紐づいてnicknameができているかを確認
        self.assertEqual(saved_nickname, 'test_nickname')

        #Categoryデータを作成
        self.category = Category.objects.create(
            name='test_category',
        )
        #self.category.save()
        category_obj = self.category
        
        

        

        #Postデータを作成
        self.post = Post.objects.create(
            author = self.user,
            category = category_obj,
            title = 'test_title',
            created = timezone.now() - datetime.timedelta(days=30),
            updated = timezone.now() - datetime.timedelta(days=10),

        )
        #self.post.save()
        
        post_obj = self.post
                       
        
        #ContentCardデータを作成
        self.contentcard = ContentCard.objects.create(
            content = 'test_content',
          #  image = im,
            post = post_obj,
        )
        
        #self.contentcard.save()


        
        

class Model_empty_Tests(TestCase):
    def test_post_is_empty(self):
        """初期状態では何も登録されていないことをチェック"""
        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 0)

    def test_category_is_empty(self):
        """Categoryデータ"""
        """初期状態では何も登録されていないことをチェック"""
        saved_categories = Category.objects.all()
        self.assertEqual(saved_categories.count(), 0)

    def test_profile_is_empty(self):
        """Profileデータ"""
        """初期状態では何も登録されていないことをチェック"""
        saved_profiles = Profile.objects.all()
        self.assertEqual(saved_profiles.count(), 0)

    def test_contentcard_is_empty(self):
        """Contentcardデータ"""
        """初期状態では何も登録されていないことをチェック"""
        saved_contentcards = ContentCard.objects.all()
        self.assertEqual(saved_contentcards.count(), 0)

class DataCountOne(LoggedInTestCase):
    
    def test_user_count_one(self):
        User = get_user_model()
        saved_user = User.objects.all()
        #ユーザーデータが１つできていることを確認
        self.assertEqual(saved_user.count(), 1)
        
    def test_profile_count_one(self):
        #Profileデータが１つできていることを確認
        saved_profile = Profile.objects.all()
        self.assertEqual(saved_profile.count(), 1)

    def test_category_count_one(self):
        #Categoryデータが１つあることを確認
        saved_category = Category.objects.all()
        self.assertEqual(saved_category.count(), 1)

    def test_post_count_one(self):
        #Postデータが1つあることを確認
        saved_post = Post.objects.all()
        self.assertEqual(saved_post.count(), 1)

    def test_contentcard_count_one(self):
        #Contentcardデータが1つあることを確認(本文のみ画像データなし)
        saved_contentcard = ContentCard.objects.all()
        sample_cc = ContentCard.objects.all()
        sample_cc=ContentCard.objects.get(content='test_content')
        print(sample_cc.content)
        self.assertEqual(saved_contentcard.count(), 1)


    #def test_post_data_create_with_contentcard(self):
    #    pt= PostFactory()
    #    print(pt.title)
#

    #def test_saving_and_retrieving_post(self):
    #    
    #    """内容を指定してデータを保存し、すぐに取り出した時に保存した時と同じ値が返されることを#テスト"""
    #    post = Post()
    #    title = 'test_title_to_retrieve'
    #    post.title = title
    #    post.save()
#
    #    saved_posts = Post.objects.all()
    #    actual_post = saved_posts[0]
#
    #    self.assertEqual(actual_post.title, title)
        

    

class ContentcardModelTests(TestCase):
    pass

    #def test_is_count_one(self):
    #    
    #    """1つレコードを適当に作成すると、レコードが1つだけカウントされることをテスト"""
    #    contentcard = ContentCard(content='test_content')
    #    contentcard.save()
    #    saved_contentcards = ContentCard.objects.all()
    #    self.assertEqual(saved_contentcards.count(), 1)
