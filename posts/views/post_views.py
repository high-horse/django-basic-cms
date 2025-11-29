# posts/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from ..models.models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.conf.urls import handler404
from django.shortcuts import render
from posts.models import Post, Category


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


# handler404 = custom_404

def post_create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        post = Post.objects.create(
            title=title,
            description=description,
            content=content,
            image=image
        )

        # Return JSON response for AJAX
        return JsonResponse({
            "status": "success",
            "message": "Post created successfully!",
            "post": {
                "id": post.id,
                "title": post.title,
                "description": post.description,
                "content": post.content,
                "image_url": post.image.url if post.image else None,
                "created_at": post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": post.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


def post_edit(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == "POST":
        post.title = request.POST.get('title')
        post.description = request.POST.get('description')
        post.content = request.POST.get('content')
        post.is_featured = 'is_featured' in request.POST

        if request.FILES.get('image'):
            post.image = request.FILES.get('image')

        post.save()

        return JsonResponse({
            "status": "success",
            "message": "Post updated successfully!",
            "post": {
                "id": post.id,
                "title": post.title,
                "description": post.description,
                "content": post.content,
                "image_url": post.image.url if post.image else None,
                "created_at": post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": post.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


# posts/views.py

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Get all comments for this post (exclude replies for now)
    # comments = Comment.objects.filter(model_type='Post', model_id=post.id).order_by('-created_at')
    category = post.category
    comments = Comment.objects.filter(model_type='Post', model_id=post.id).order_by('-created_at')

    context = {
        'post': post,
        'comments': comments,
        'category_name': category.name,  
        'category_id': category.id 
    }
    return render(request, 'post_detail.html', context)


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == "POST":
        post.delete()
        return JsonResponse({"status": "success", "message": "Post deleted successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

def home(request):
    # Fetch all categories ordered by name
    categories = Category.objects.all().order_by('name')

    # Get the selected categories from the URL query parameters
    selected_categories = request.GET.get('categories', '')
    selected_categories_list = [c.strip() for c in selected_categories.split(',') if c.strip()]

    # Fetch featured posts
    featured_posts = Post.objects.filter(is_featured=True).select_related('category')
    
    # Fetch other posts, excluding the featured ones
    other_posts = Post.objects.exclude(
        id__in=featured_posts.values_list('id', flat=True)
    ).select_related('category').order_by('-created_at')

    # Filter both featured and other posts by selected categories if any
    if selected_categories_list:
        featured_posts = featured_posts.filter(category__name__in=selected_categories_list)
        other_posts = other_posts.filter(category__name__in=selected_categories_list)

    # Render the page with filtered posts and selected categories
    return render(request, 'home.html', {
        "title": "My First Django Page",
        "username": "Camel",
        "numbers": [1, 2, 3, 4],
        "featured_posts": featured_posts,
        "posts": other_posts,
        "categories": categories,
        "selected_categories": selected_categories_list,  # This is passed to the template and JS
    })


# views.py (already good — just confirming)
def home__(request):
    categories = Category.objects.all().order_by('name')
    selected_categories = request.GET.get('categories', '')
    selected_categories_list = [c.strip() for c in selected_categories.split(',') if c.strip()]

    featured_posts = Post.objects.filter(is_featured=True).select_related('category')
    
    other_posts = Post.objects.exclude(
        id__in=featured_posts.values_list('id', flat=True)
    ).select_related('category').order_by('-created_at')

    if selected_categories_list:
        other_posts = other_posts.filter(category__name__in=selected_categories_list)

    return render(request, 'home.html', {
        "title": "My First Django Page",
        "username": "Camel",
        "numbers": [1, 2, 3, 4],
        "featured_posts": featured_posts,
        "posts": other_posts,
        "categories": categories,
        "selected_categories": selected_categories_list,  # ← used in template + JS
    })
    
    
    
def home_(request):
    # Get the featured post (assuming only one featured post)
    featured_posts = Post.objects.filter(is_featured=True)

    # Get all other posts excluding the featured one
    if featured_posts.exists():
        other_posts = Post.objects.exclude(id__in=featured_posts.values_list('id', flat=True)).order_by('-created_at')
    else:
        other_posts = Post.objects.all().order_by('-created_at')

    # Optional: Prefetch category to avoid extra queries
    featured_posts = featured_posts.select_related('category')
    other_posts = other_posts.select_related('category')
    
    categories = Category.objects.all().order_by('name') 
    
    context = {
        "title": "My First Django Page",
        "username": "Camel",
        "numbers": [1, 2, 3, 4],
        "featured_posts": featured_posts,
        "posts": other_posts,
        "categories": categories,
    }
    return render(request, 'home.html', context)



def manage(request):
    posts = Post.objects.all()
    return render(request, 'manage.html', {"posts": posts})


@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        content = request.POST.get("content")
        username = request.user.username

        # Use generic fields to link to the post
        Comment.objects.create(
            username=username,
            content=content,
            model_type="Post",   # the model name
            model_id=post_id     # the id of the post
        )

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error", "message": "Invalid request"})


def add_reply(request, comment_id):
    if request.method == 'POST':
        parent_comment = get_object_or_404(Comment, id=comment_id)

        username = request.POST.get("username")
        content = request.POST.get('content')

        Comment.objects.create(
            username=username,
            content=content,
            model_type='Comment',
            model_id=parent_comment.id,
        )

        return JsonResponse({"status": "success", "message": "Reply added successfully."})

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)


def register_view(request):
    from django.shortcuts import render, redirect
    from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
    from django.contrib.auth import login

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    from django.shortcuts import render, redirect
    from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
    from django.contrib.auth import login

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('posts:list')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})