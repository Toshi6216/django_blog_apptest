from django.test import TestCase
from blog.models import Post, Category, Profile, ContentCard

class PostModelTests(TestCase):
    def test_is_empty(self):
        
        """初期状態では何も登録されていないことをチェック"""
        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 0)

    #def test_is_count_one(self):
    #    
    #    """1つレコードを適当に作成すると、レコードが1つだけカウントされることをテスト"""
    #    post = Post(title='test_title')
    #    post.save()
    #    saved_posts = Post.objects.all()
    #    self.assertEqual(saved_posts.count(), 1)

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
        

class CategoryModelTests(TestCase):
    def test_is_empty(self):
        """Categoryデータ"""
        """初期状態では何も登録されていないことをチェック"""
        saved_categories = Category.objects.all()
        self.assertEqual(saved_categories.count(), 0)

    #def test_is_count_one(self):
    #    """Categoryデータ"""
    #    """1つレコードを適当に作成すると、レコードが1つだけカウントされることをテスト"""
    #    category = Category(name='test_name')
    #    category.save()
    #    saved_categories = Category.objects.all()
    #    self.assertEqual(saved_categories.count(), 1)

class ProfileModelTests(TestCase):
    def test_is_empty(self):
        """Profileデータ"""
        """初期状態では何も登録されていないことをチェック"""
        saved_profiles = Profile.objects.all()
        self.assertEqual(saved_profiles.count(), 0)

    #def test_is_count_one(self):
    #    
    #    """1つレコードを適当に作成すると、レコードが1つだけカウントされることをテスト"""
    #    profile = Profile(nickname='test_nickname')
    #    profile.save()
    #    saved_profiles = Profile.objects.all()
    #    self.assertEqual(saved_profiles.count(), 1)

    

class ContentcardModelTests(TestCase):
    def test_is_empty(self):
        """Contentcardデータ"""
        """初期状態では何も登録されていないことをチェック"""
        saved_contentcards = ContentCard.objects.all()
        self.assertEqual(saved_contentcards.count(), 0)

    #def test_is_count_one(self):
    #    
    #    """1つレコードを適当に作成すると、レコードが1つだけカウントされることをテスト"""
    #    contentcard = ContentCard(content='test_content')
    #    contentcard.save()
    #    saved_contentcards = ContentCard.objects.all()
    #    self.assertEqual(saved_contentcards.count(), 1)
