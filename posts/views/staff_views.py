from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect,  get_object_or_404
from ..models import Post, Comment, Category
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

User = get_user_model()


def staff_required(view_func):
    # return user_passes_test(lambda u: u.is_authenticated and u.is_staff)(view_func)
    return user_passes_test(lambda u: u.is_staff, login_url='/staff/login/')(view_func)



@staff_required
def dashboard(request):
    context = {
        'posts_count': Post.objects.count(),
        'comments_count': Comment.objects.count(),
        'categories_count': Category.objects.count(),
        'users_count': User.objects.count(),
    }
    return render(request, "staff/dashboard.html", context)



@staff_required
def post_list(request):
    posts_qs = Post.objects.all()
    paginator = Paginator(posts_qs, 10)  # 10 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()  # For create/edit category select
    return render(request, "staff/post_list.html", {
        "page_obj": page_obj,
        "categories": categories
    })

@staff_required
def post_create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        is_featured = 'is_featured' in request.POST

        category = Category.objects.filter(id=category_id).first() if category_id else None

        post = Post.objects.create(
            title=title,
            description=description,
            content=content,
            category=category,
            image=image,
            is_featured=is_featured
        )

        return JsonResponse({
            "status": "success",
            "message": "Post created successfully!",
            "post": {
                "id": post.id,
                "title": post.title,
                "description": post.description,
                "content": post.content,
                "category": post.category.name if post.category else None,
                "image_url": post.image.url if post.image else None,
                "is_featured": post.is_featured,
                "created_at": post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": post.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
        })

    # Fix: If someone makes a GET request, just redirect to the posts list
    return redirect('staff_posts')



@staff_required
def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        post.title = request.POST.get("title")
        post.description = request.POST.get("description")
        post.content = request.POST.get("content")
        post.is_featured = "is_featured" in request.POST

        category_id = request.POST.get("category")
        post.category = Category.objects.filter(id=category_id).first() if category_id else None

        if request.FILES.get("image"):
            post.image = request.FILES.get("image")
        post.save()

        return JsonResponse({
            "success": True,
            "id": post.id,
            "title": post.title,
            "description": post.description or "",
            "content": post.content or "",
            "category_name": post.category.name if post.category else "",
            "is_featured": post.is_featured
        })
    return JsonResponse({"success": False}, status=400)


@staff_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        post.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)



@staff_required
def categories(request):
    category_list = Category.objects.all().order_by('-id')
    paginator = Paginator(category_list, 10)  # 10 categories per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "staff/categories_list.html", {"page_obj": page_obj})


@staff_required
def create_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        category = Category.objects.create(name=name, desc=desc)
        return JsonResponse({"success": True, "id": category.id, "name": category.name})
    return JsonResponse({"success": False}, status=400)

@staff_required
def edit_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == "POST":
        category.name = request.POST.get("name")
        category.desc = request.POST.get("desc")
        category.save()
        return JsonResponse({"success": True, "id": category.id, "name": category.name})
    return JsonResponse({"success": False}, status=400)

@staff_required
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return JsonResponse({"success": True})



@staff_required
def comment_list(request):
    comments_qs = Comment.objects.all().order_by('-created_at')
    paginator = Paginator(comments_qs, 10)  # 10 comments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "staff/comment_list.html", {
        "page_obj": page_obj
    })


@staff_required
def comment_delete(request, id):
    comment = get_object_or_404(Comment, id=id)
    if request.method == "POST":
        comment.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


@staff_required
def user_list(request):
    users_qs = User.objects.all().order_by('id')
    paginator = Paginator(users_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "staff/user_list.html", {"page_obj": page_obj})


@staff_required
def user_create(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        is_staff = "is_staff" in request.POST

        user = User.objects.create(
            username=username,
            email=email,
            is_staff=is_staff
        )

        return JsonResponse({
            "status": "success",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": "Staff" if user.is_staff else "Guest"
            }
        })
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


@staff_required
def user_edit(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.is_staff = "is_staff" in request.POST
        user.save()
        return JsonResponse({
            "status": "success",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": "Staff" if user.is_staff else "Guest"
            }
        })
    return JsonResponse({"status": "error"}, status=400)


@staff_required
def user_delete(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == "POST":
        user.delete()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)