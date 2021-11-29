from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse

# Create your models here.

class ProfileManager(models.Manager):
    
    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

class Profile(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='No bio...')
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"pk": self.pk})

    def get_friends(self):
        return self.friends.all()

    def get_friends_n(self):
        return self.friends.all().count()

    def get_posts_n(self):
        return self.posts.all().count()

    def get_all_author_posts(self):
        return self.posts.all()

    def get_likes_given_n(self):
        likes = self.like_set.all()
        total_liked = 0 
        for item in likes:
            if item.value == 'Like':
                total_liked += 1
        return total_liked
    
    def get_likes_received_n(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked

    def __str__(self):
        return f"{self.user.username} - {self.created.strftime('%d-%m-%Y')}"

    
    
        


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)

class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = RelationshipManager()


    def __str__(self):
        return f"{self.sender} - {self.receiver} - {self.status}"