# posts/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Post, Comment

from django.conf.urls import handler404
from django.shortcuts import render


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
    comments = Comment.objects.filter(model_type='Post', model_id=post.id).order_by('-created_at')

    context = {
        'post': post,
        'comments': comments
    }
    return render(request, 'post_detail.html', context)

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == "POST":
        post.delete()
        return JsonResponse({"status": "success", "message": "Post deleted successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


def home(request):
    # Get the featured post (assuming only one featured post)
    featured_posts = Post.objects.filter(is_featured=True)

    # Get all other posts excluding the featured one
    if featured_posts.exists():
        other_posts = Post.objects.exclude(id__in=featured_posts.values_list('id', flat=True)).order_by('-created_at')
    else:
        other_posts = Post.objects.all().order_by('-created_at')

    context = {
        "title": "My First Django Page",
        "username": "Camel",
        "numbers": [1, 2, 3, 4],
        "featured_posts": featured_posts,
        "posts": other_posts
    }
    return render(request, 'home.html', context)


def home_(request):
    posts = Post.objects.all()
    context = {
        "title": "My First Django Page",
        "username": "Camel",
        "numbers": [1, 2, 3, 4],
        "posts": posts
    }
    return render(request, 'home.html', context)


def manage(request):
    posts = Post.objects.all()
    return render(request, 'manage.html', {"posts": posts})


def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)

        username = request.POST.get('username')
        content = request.POST.get('content')

        Comment.objects.create(
            username=username,
            content=content,
            model_type='Post',
            model_id=post.id,
        )
        return JsonResponse({"status": "success", "message": "Comment added successfully."})

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)


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
