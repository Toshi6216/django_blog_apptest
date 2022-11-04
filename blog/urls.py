from django.urls import path
from blog import views

urlpatterns = [
    path('blog/', views.IndexView.as_view(), name='index'),
    path('category_form/', views.categoryFormView, name='category_form'),
    path('category_delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('post/<int:pk>/detail/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.CreatePostView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('category/<str:category>/', views.CategoryView.as_view(), name='category'),

    path('test/<int:pk>/detail/', views.TestDetailView.as_view(), name='test_detail'),
    path('test/', views.BlogTestView.as_view(), name='test'),
    path('sample/', views.lists, name='lists'),
]
