from django.test import TestCase, Client
from django.urls import reverse, resolve, reverse_lazy
from ..views import LoginView, LogoutView 
from ...blog.tests.test_urls import LoggedInTestCase

class TestUrlsWithLogin(LoggedInTestCase):


    """loginページへのURLでアクセスする時のリダイレクトをテスト"""
    def test_login_url(self):
        view = resolve('/accounts/login/')
        self.assertEqual(view.func.view_class, LoginView)

    """loginページのステータスコードをテスト"""
    def test_login_view_status_code(self):
        url = reverse('account_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)