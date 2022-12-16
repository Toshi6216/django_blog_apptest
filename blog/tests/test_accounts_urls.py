from django.test import TestCase, Client
from django.urls import reverse, resolve, reverse_lazy
from accounts.views import LoginView, LogoutView, ProfileView, newSignupView 
from .test_urls import LoggedInTestCase
from django.contrib.auth import get_user_model

class TestAccountsWithLogin(LoggedInTestCase):
    """loginページへのURLでアクセスする時のリダイレクトをテスト(すでにログインしているのでindexページにリダイレクトされる)"""
    def test_login_url_with_login(self):
        view = resolve('/accounts/login/')
        self.assertEqual(view.func.view_class, LoginView)

    def test_login_url_with_login2(self):
        response = self.client.get(reverse_lazy('account_login'))
        self.assertRedirects(response, '/blog/')
        

    """logoutページへのURLでアクセスする時のリダイレクトをテスト"""
    def test_logout_url(self):
        view = resolve('/accounts/logout/')
        self.assertEqual(view.func.view_class, LogoutView)

    def test_logout_url2(self):
        """logoutページのステータスコードをテスト"""
        url = reverse('account_logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print("test_logout_url")

    def test_profile_url(self):
        """profileページのステータスコードをテスト"""
        user = get_user_model().objects.get(username="test_user")
        url = reverse('profile', kwargs={'pk': user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print("test_profile_url")

class LoginSignupViewTest(TestCase):
    """loginページのステータスコードをテスト"""
    def test_login_view_status_code(self):
        url = reverse('account_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print("test_login_view_status_code")

 
    def test_signup_view_status_code_with_logout(self):
        """サインアップページの表示テスト"""
        url = reverse('account_signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print("test_signup_view_status_code")

    def test_signup_url(self):
        """signupページへのURLでアクセスする時のリダイレクトをテスト"""
        view = resolve('/accounts/signup/')
        print(view.func)
        self.assertEqual(view.func, newSignupView)

