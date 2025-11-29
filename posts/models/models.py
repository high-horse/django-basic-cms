from django.db import models
from django.utils.text import slugify
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # renamed for consistency
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="posts/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "posts"
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    username = models.CharField(max_length=255)
    content = models.TextField()

    # Generic relation (model_type/model_id)
    model_type = models.CharField(max_length=255)
    model_id = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comments"

    def __str__(self):
        return f"Comment by {self.username} on {self.model_type}"

    def is_reply(self):
        return self.model_type.lower() == "comment"

    def get_related_object(self):
        from django.apps import apps
        model_class = apps.get_model(app_label='posts', model_name=self.model_type)
        return model_class.objects.get(id=self.model_id)
