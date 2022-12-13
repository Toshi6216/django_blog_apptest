import datetime
from django.test import TestCase, Client
from .test_models import LoggedInTestCase
from django.urls import reverse, resolve, reverse_lazy
from .test_models import LoggedInTestCase
from blog.models import Post, Category, Profile, ContentCard

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
print(now)

class IndexViewTests(TestCase):
    """IndexViewのレスポンスを検証"""
    def test_get(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        print("IndexView test_get")


class DetailViewTests(LoggedInTestCase):
    """DetailViewのレスポンスを検証"""
    def test_get(self):
        post = Post.objects.get(title='test_title')
        url = reverse('post_detail', args=(post.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print("DetailPostView test_get")


class CreatePostViewTests(LoggedInTestCase):
    """CreatePostViewのレスポンスを検証"""
    def test_get(self):
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 200)
        print("CreatePostView test_get")

    """記事投稿の成功を検証"""
    def test_post_success(self):
        #postデータを生成
        params = {
            "author": 1,
            "category": 1,
            "title": "post test",
            "created": "2022-12-07T02:29:59.511Z",
            "updated": "2022-12-07T05:29:09.338Z",

            }
        response = self.client.post(reverse_lazy('post_new'), params)
        #indexへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('index'))
        #データベースへ登録されたことを検証
        self.assertEqual(Post.objects.filter(title='post test').count(), 1)

    """ログアウト時に投稿できないことを検証"""
    def test_post_error(self):
        self.client.logout()
        params = {
            "author": 1,
            "category": 1,
            "title": "post test",
            "created": "2022-12-07T02:29:59.511Z",
            "updated": "2022-12-07T05:29:09.338Z",

            }
        response = self.client.post(reverse_lazy('post_new'), params)

         # ログインページへのリダイレクトを検証
        self.assertRedirects(response, 'accounts/login/?next=/post/new')
        #データベースへ登録されたことを検証
        self.assertEqual(Post.objects.filter(title='post test').count(), 0)

class PostEditViewTests(LoggedInTestCase):

    def test_get(self):
        post = Post.objects.get(title='test_title')
        url = reverse('post_detail', args=(post.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print("PostEditView test_get")

        #self.assertRedirects(response, reverse_lazy('post_edit', kwargs={'pk':post.pk}))