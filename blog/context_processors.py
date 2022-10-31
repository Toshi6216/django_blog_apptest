from .models import Category, Post

def common(request):
    category_data = Category.objects.all()
#    posts_data = Post.objects.all()
    posts_data = Post.objects.order_by('-id')
    posts_data2 = Post.objects.order_by('-id')[:5]
    for_range = [i for i in range(3)]

    context = {
        'category_data' : category_data,
        'posts_data' : posts_data,
        'for_range': for_range,
    }
        
    
    return context