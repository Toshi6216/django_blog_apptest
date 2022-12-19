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
        print("DetailView test_get")


class CreatePostViewTests(LoggedInTestCase):
    """CreatePostViewのレスポンスを検証"""
    def test_get(self):
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 200)
        print("CreatePostView test_get")
        print(f"author:{Post.objects.get(pk=1).author}")

    """記事投稿の成功を検証"""
    def test_post_success(self):
        #postデータを生成
        #category=Category.objects.get(pk=1)
        params = {
            "author": self.user,
            "category": 1,
            "title": "post test",
            "created": timezone.now() - datetime.timedelta(days=30),
            "updated": timezone.now(),

            }
        response = self.client.post(reverse_lazy('post_new'), params)
        post_data=Post.objects.get(title='post test')
        #print(f"new post category:{post_data.category}")
        post_data_all = Post.objects.all()
        
        #indexへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('index'))
        #データベースへ登録されたことを検証
        post_data=Post.objects.filter(title='post test')
        self.assertEqual(post_data.count(), 1)
        
    """ログアウト時に投稿できないことを検証"""
    def test_post_error(self):
        self.client.logout()
        params = {
            "author": self.user,
            "category": 1,
            "title": "post test",
            "created": timezone.now() - datetime.timedelta(days=30),
            "updated": timezone.now()

            }
        
        response = self.client.post(reverse_lazy('post_new'), params)
        
         # ログインページへのリダイレクトを検証
        self.assertRedirects(response, '/accounts/login/?next=/post/new/')
        #データベースへ登録されたことを検証
        self.assertEqual(Post.objects.filter(title='post test').count(), 0)
        print("CreatePostView test_post_error")

class PostEditViewTests(LoggedInTestCase):
    #記事編集画面のテスト
    def test_get(self):
        """ログイン時編集編集画面へのアクセス(author=user)を確認"""
        post = Post.objects.get(title='test_title')
        url = reverse('post_edit', args=(post.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print("PostEditView test_get")

    def test_edit_and_redirect(self):
        """ログイン時、編集できること、リダイレクトを確認"""
        print(f"post login user: {self.user}")
        post = Post.objects.get(title='test_title')
        
        data={
            "author": self.user,
            "category": 1,
            "title": "post_edited_test",
            "updated": timezone.now(),
            #"content": "edited_content",

        }
        url=reverse_lazy('post_edit', kwargs={'pk': post.pk})
        print(f"reverse_lazy:{url}")

        response = self.client.post(reverse_lazy('post_edit', kwargs={'pk': post.pk}), data)
        # データが編集されたことを検証
        post_updated = Post.objects.get(pk=post.pk)
        print(f"post updated title: {post_updated.title}")
        self.assertEqual(post_updated.title, "post_edited_test")
        
        # indexページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('index'))
        print("PostEditView test_redirect")

class PostEditViewTests_with_Logout(LoggedInTestCase):
    def test_edit_error_with_logout(self):
        """ログアウト時編集編集画面へのアクセス不可を確認"""
        self.client.logout()
        post = Post.objects.get(title='test_title')
        url = reverse('post_edit', args=(post.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        print("PostEditView test_edit_error_with_logout")

class PostEditViewTests_defferent_author(LoggedInTestCase):
    def test_edit_error_defferent_author(self):
        """"ユーザーと異なるauthorの記事の編集画面へのアクセス不可を確認"""
        #テストユーザー2作成
        self.password='password2'
        User = get_user_model()
        self.user = User.objects.create_user(
            username='test_user2',
            email='test2@aaa.ccc',
            password=self.password,
         )
        user_obj=self.user
        #作成したユーザーデータでログイン
        self.client.login(
            username=user_obj.username,
            password=self.password,
        )
        #記事のauthorとは別のuserで編集ページにアクセスするとエラーとなることを確認
        post = Post.objects.get(title='test_title')
        url = reverse('post_edit', args=(post.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        print("PostEditView test_edit_error_defferent_author")

class PostDeleteViewTests(LoggedInTestCase):
    """投稿記事削除ページのテスト"""
    def test_post_delete_url_error_with_login(self):
        """投稿記事削除ページの表示（ログイン時）"""
        post = Post.objects.get(title='test_title')
        url = reverse('post_delete', args=(post.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print("PostDeleteView test_post_delete_url")

    def test_post_delete_success_with_login(self):
        #ログイン状態でないとカテゴリ削除できない
        #削除対象読み込み
        delete_post = Post.objects.get(title="test_title")
        print(f"delete post: {delete_post}")

        #削除実行
        response = self.client.post(reverse_lazy("post_delete", kwargs={"pk":delete_post.pk}))
                
        confirm_post_delete = Post.objects.all()
        #投稿記事が減り、ないことを確認
        self.assertEqual(confirm_post_delete.count(), 0)
        print("test_post_delete_success_with_login_post_delete_success")
         
class PostDeleteViewTests_with_logout(LoggedInTestCase):
    """ログアウト時、投稿削除ページへアクセスするとリダイレクトされるのをテスト"""
    def test_postdelete_url_error_with_logout(self):
        self.client.logout()
        post = Post.objects.get(title='test_title')
        url = reverse('post_delete', args=(post.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        print("PostDeleteView test_post_delete_url_with_logout_access_error")


class CategoryViewTests(LoggedInTestCase):
    #カテゴリ別画面のテスト
    def test_get(self):
        category = Category.objects.get(name='test_category')
        url = reverse('category', args=(category.name,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        #print(url)
        print("CategoryView test_get")

class CategoryFormViewTests(LoggedInTestCase):
    """カテゴリ追加フォームのテスト"""
    def test_categoryform_url_error_with_login(self):
        response = self.client.get(reverse('category_form'))
        self.assertEqual(response.status_code, 200)
        print("CategoryFormView test_category_form_url")

    def test_category_form_input_success_with_login(self):
        #ログイン状態でないとカテゴリ追加できない
        #categoryデータを生成
        params = {
            "name": "test_category_post_test"
            }
        response = self.client.post(reverse_lazy('category_form'), params)
        category_data_all=Category.objects.all()
        count=category_data_all.count()
        
        #データベースへ登録されたことを検証
        category_data=Category.objects.filter(name="test_category_post_test")
        self.assertEqual(category_data.count(), 1)
        #カテゴリが増えて２つあることを確認
        self.assertEqual(count, 2)
        print("category_post_success")

    def test_categoryform_url_error_with_logout(self):
        self.client.logout()
        response = self.client.get(reverse('category_form'))
        self.assertEqual(response.status_code, 302)
        print("CategoryFormView test_category_form_url_with_logout")
        
class CategoryDeleteViewTests(LoggedInTestCase):
    """カテゴリ削除フォームのテスト"""
    def test_category_delete_url_error_with_login(self):
        response = self.client.get(reverse('category_delete'))
        self.assertEqual(response.status_code, 200)
        print("CategoryDeleteView test_category_delete_url")

    def test_category_form_delete_success_with_login(self):
        #ログイン状態でないとカテゴリ削除できない
        #削除対象読み込み
        delete_category = Category.objects.get(pk=1)
        print(f"delete category: {delete_category}")
        param={
            "pk":1
        }
        #削除実行
        response = self.client.post(reverse_lazy("category_delete"), param)
        #response = self.client.post(reverse_lazy("category_delete", kwargs={"pk":delete_category.pk}))
        
        confirm_delete = Category.objects.all()
        #カテゴリが減り、ないことを確認
        self.assertEqual(confirm_delete.count(), 0)
        print("test_category_form_delete_success_with_login")
         

    def test_categorydelete_url_error_with_logout(self):
        self.client.logout()
        response = self.client.get(reverse('category_delete'))
        self.assertEqual(response.status_code, 302)
        print("CategoryFormView test_category_delete_url_with_logout")


        