from django.test import TestCase, Client
from django.urls import reverse, resolve, reverse_lazy
from ..views import IndexView, categoryFormView, CategoryDeleteView, CreatePostView, CategoryView, PostDetailView

from ..models import Category, Post
from django.contrib.auth import get_user_model
#from .factories import UserFactory

class LoggedInTestCase(TestCase):
    def setUp(self):
        #テストユーザー作成
        self.password='password'
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@aaa.ccc',
            password=self.password,
            
         )
        #self.user = UserFactory()

        self.client=Client()
        #ログイン
        self.client.login(
            username=self.user.username,
            password=self.password,
        )

        #fixtures = ['/home/toshi/work/code_django/product_code/blog_apptest/fixture.json']
        

        #self.category = Category.objects.create(
        #    name='test_cat',
        #)
        
        #self.post = Post.objects.create(
        #    auther = 'test_user',
        #    category = Category.objects.get_or_create(name='test_cat')#[0],
        #    title = 'test_title',
        #)

    #def add_category():
    #    c = Category.objects.get_or_create(name='test_category')[0]
    #    c.save()
    #    return c

class TestUrlsWithLogin(LoggedInTestCase):
    

    """indexページへのURLでアクセスする時のリダイレクトをテスト"""
    def test_index_url(self):
        view = resolve('/blog/')
        self.assertEqual(view.func.view_class, IndexView)

    """Indexページのステータスコードをテスト"""
    def test_index_view_status_code(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    """category_formページへのURLでアクセスする時のリダイレクトをテスト"""
    def test_category_form_url(self):
        view = resolve('/category_form/')
        self.assertEqual(view.func, categoryFormView)

    """category_formページのステータスコードをテスト"""
    def test_category_form_view_status_code(self):
        url = reverse('category_form')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    """カテゴリ作成の成功をテスト"""
    def test_category_imput(self):
        params = {'name':'test_category',}
        response = self.client.post(reverse_lazy('category_form'), params)
        print("//category//")
        print(Category.objects.filter(name='test_category'))

        self.assertRedirects(response, reverse_lazy('category_form'))
        self.assertEqual(Category.objects.filter(name='test_category').count, 1)
        


    """category_deleteページへのURLでアクセスする時のリダイレクトをテスト"""
    def test_category_delete_url(self):
        view = resolve('/category_delete/')
        self.assertEqual(view.func.view_class, CategoryDeleteView)

    """category_deleteページのステータスコードをテスト"""
    def test_category_delete_view_status_code(self):
        url = reverse('category_delete')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    """post_newページへのURLでアクセスする時のリダイレクトをテスト"""
    def test_post_new_url(self):
        view = resolve('/post/new/')
        self.assertEqual(view.func.view_class, CreatePostView)

    """post_newページのステータスコードをテスト"""
    def test_create_post_view_status_code(self):
        url = reverse('post_new')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    
