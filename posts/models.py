from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile

# Create your models here.
class Post(models.Model):
    content = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='posts', blank=True, validators=[FileExtensionValidator('png', 'jpg','jpeg')])
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts', default=None)

    def __str__(self):
        return f"{self.content[:12]}"

    def num_likes(self):
        return self.liked.all().count()

    def num_comments(self):
        return self.comment_set.all().count()

    def get_comments(self):
        return self.comment_set.all()

    class Meta:
        ordering = ['-created',]

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.post} -> {self.body[:5]}"

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
)

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(max_length=8, choices=LIKE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.post} - {self.value}"