from .models import Category, Post

def common(request):
    category_data = Category.objects.all()
    posts_data = Post.objects.order_by('-id')
    posts_data2 = Post.objects.order_by('-id')[:5]
    

    context = {
        'category_data' : category_data,
        'posts_data' : posts_data,
        'posts_data2' : posts_data2,
    }
        
    
    return context