from cProfile import Profile
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

MAX_SIZE    = 2 * 1000 * 1000

def validate_max_size(value):
    if value.size > MAX_SIZE:
        raise ValidationError( "ファイルサイズが上限(" + str(MAX_SIZE/1000000) + "MB)を超えています。送信されたファイルサイズ: " + str(value.size/1000000) + "MB")
    else:
        print("問題なし")

#カテゴリのモデル
class Category(models.Model):
    name = models.CharField(
        'カテゴリ',
        max_length=100,
        unique=True,        
        )
   
    def __str__(self):
        return self.name


#ニックネーム設定用モデル
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True,
    )

    def __str__(self):
        return self.nickname

#投稿記事のモデル
class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    category = models.ForeignKey(
        Category,
        verbose_name='カテゴリ',       
        on_delete=models.PROTECT
    )

    title = models.CharField(
        "タイトル", 
        max_length=200,
        blank=False,
        null=False)
    image = models.ImageField(
        upload_to='images', 
        verbose_name='イメージ画像', 
        null=True,
        blank=True
    )

    content = models.TextField(
        "本文",
        blank=True,
        null=False)
    created = models.DateTimeField(
        "作成日", 
        auto_now_add=True,
        editable=False,
        blank=False,
        null=False)
    updated = models.DateTimeField(
        "更新日",
        auto_now=True,
        editable=False,
        blank=False,
        null=False)
    
    
    def __str__(self):
        return self.title

#本文とimgのセット
class ContentCard(models.Model):
    content = models.TextField()
    image = models.ImageField(
        upload_to='images', 
        verbose_name='イメージ画像', 
        null=True,
        blank=True,
        validators=[validate_max_size],
    )
    post = models.ForeignKey(
        Post, verbose_name = '紐づく記事',
        related_name = "contentcard",
        on_delete = models.CASCADE
    )
    def __str__(self):
        return self.post.title


