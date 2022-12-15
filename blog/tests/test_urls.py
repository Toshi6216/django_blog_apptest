from django.test import TestCase, Client
from django.urls import reverse, resolve, reverse_lazy
from ..views import IndexView, categoryFormView, CategoryDeleteView, CreatePostView, CategoryView, PostDetailView
from django.utils import timezone
import datetime
from ..models import Category, Post
from django.contrib.auth import get_user_model
#from .factories import UserFactory
from .test_models import LoggedInTestCase


class TestUrlsWithLogin(LoggedInTestCase):
      

    """Indexページのステータスコードをテスト"""
    def test_index_view_status_code(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print("test_index_view_status_code")
        


    """category_formページへのURLでアクセスする時のリダイレクトをテスト"""
    def test_category_form_url(self):
        view = resolve('/category_form/')
        self.assertEqual(view.func, categoryFormView)
        print("test_category_form_url")

    """category_formページのステータスコードをテスト"""
    def test_category_form_view_status_code(self):
        url = reverse('category_form')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print("test_category_form_view_status_code")

    """カテゴリ作成の成功をテスト"""
    def test_category_imput(self):
        params = {'name':'test_category2',}
        response = self.client.post(reverse_lazy('category_form'), params)
        qs_counter2 = Category.objects.count()
        #カテゴリ追加後の画面表示を検証
        self.assertEqual(response.status_code, 200)
        #データベースへの登録を検証（カテゴリ件数2個になっていることを確認）
        self.assertEqual(qs_counter2, 2)
        print("test_category_imput")
    

    """category_deleteページへのURLでアクセスする時のリダイレクトをテスト"""
    def test_category_delete_url(self):
        view = resolve('/category_delete/')
        self.assertEqual(view.func.view_class, CategoryDeleteView)
        print("test_category_delete_url")

    """category_deleteページのステータスコードをテスト"""
    def test_category_delete_view_status_code(self):
        url = reverse('category_delete')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print("test_category_delete_view_status_code")

    """投稿(post_new)ページへのURLでアクセスする時のリダイレクトをテスト"""
    def test_post_new_url(self):
        view = resolve('/post/new/')
        self.assertEqual(view.func.view_class, CreatePostView)
        print("test_post_new_url")

    """投稿(post_new)ページのステータスコードをテスト"""
    def test_create_post_view_status_code(self):
        url = reverse('post_new')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print("test_create_post_view_status_code")


    """detailページのステータスコード(成功)をテスト"""
    def test_post_detail_view_status_code(self):
        post = Post.objects.get(title = 'test_title')
        url = reverse('post_detail', kwargs={'pk': post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print("test_post_detail_view_status_code")

    #"""detailページのステータスコード(存在しないページでエラー)をテスト"""
    #def test_post_detail_view_status_code_404(self):
    #   
    #    url = reverse('post_detail', kwargs={'pk': 10})
    #    response = self.client.get(url)
    #    self.assertEqual(response.status_code, 404)


