from django.db import models
from django.utils.text import slugify

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    image = models.ImageField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        db_table= 'posts'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def save(self, *args, **kwargs):
        if not self.slug:  # Only create slug if it doesn't exist
            self.slug = slugify(self.title)
            
            # Ensure slug is unique
            original_slug = self.slug
            queryset = Post.objects.filter(slug=self.slug)
            counter = 1
            while queryset.exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
                queryset = Post.objects.filter(slug=self.slug)

        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    username = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    model_type = models.CharField(max_length=255, null=True, blank=True)
    model_id = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comments"

    def __str__(self):
        return f"Comment by {self.username} on {self.model_type}"

    def is_reply(self):
        return self.model_type == "Comment"

    def get_related_object(self):
        from django.apps import apps
        model_class = apps.get_model(app_label='posts', model_name=self.model_type)
        return model_class.objects.get(id=self.model_id)