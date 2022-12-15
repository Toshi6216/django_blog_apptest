import datetime
from django.test import TestCase, Client
from .test_models import LoggedInTestCase
from django.urls import reverse, resolve, reverse_lazy
from .test_models import LoggedInTestCase
from blog.models import Post, Category, Profile, ContentCard
from django.contrib.auth import get_user_model
from PIL import Image
from ..forms import PostForm, ContentCardForm, CardFormset, CategoryForm

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
        post_data=Post.objects.get(title='post test')
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
            "author": 1,
            "category": 1,
            "title": "post test",
            "created": "2022-12-07T02:29:59.511Z",
            "updated": "2022-12-07T05:29:09.338Z",

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
        post = Post.objects.get(title='test_title')
        
    #    img = Image.new('RGB', (200, 150), 'yellow')
    #    img.save('media/images/sample2.jpg')
        
        data={
            "author": 1,
            "category": 1,
            "title": "post_edited_test",
            "created": "2022-12-07T02:29:59.511Z",
            "updated": "2022-12-07T05:29:09.338Z",
            "content":"test",
            "image": "",
            #"content":"content_edited_test",
            #"image": "media/images/sample2.jpg",
        }
        url=reverse_lazy('post_edit', kwargs={'pk': post.pk})
        print(f"reverse_lazy:{url}")
        response = self.client.post(reverse_lazy('post_edit', kwargs={'pk': post.pk}), data)
        
        # データが編集されたことを検証
        post_updated = Post.objects.get(pk=post.pk)
        
        self.assertEqual(post_updated.title, "post_edited_test")
        
        # indexページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('index'))
        print("PostEditView test_redirect")

    def test_edit_error_with_logout(self):
        """ログアウト時編集編集画面へのアクセス不可を確認"""
        self.client.logout()
        post = Post.objects.get(title='test_title')
        url = reverse('post_edit', args=(post.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        print("PostEditView test_edit_error_with_logout")

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
    def test_post_success(self):
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
        print("category_post_success")

    def test_step1_form(self):
        data = {
            "name":"category_name_test2"
        }
        
        form = CategoryForm(data)
        self.assertTrue(form.is_valid())
        print("category form is valid")

        