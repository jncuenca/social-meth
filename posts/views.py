from django.core.checks import messages
from django.shortcuts import redirect, render
#from django.views.generic.edit import UpdateView
from .models import Post, Like
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
@login_required
def main_post_view(request):
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    
    #initial forms
    p_form = PostModelForm()
    c_form = CommentModelForm()

    if request.method == 'POST':
        print(request)
        if "submit_p_form" in request.POST:
            p_form = PostModelForm(request.POST, request.FILES)
            if p_form.is_valid():
                instance = p_form.save(commit=False)
                instance.author = profile
                instance.save()
                p_form = PostModelForm() #reset the form

        if "submit_c_form" in request.POST:
            c_form = CommentModelForm(request.POST)
            if c_form.is_valid():
                instance = c_form.save(commit=False)
                instance.user = profile
                instance.post = Post.objects.get(id=request.POST['post_id'])
                instance.save()
                c_form = CommentModelForm() #reset the form

    context = {
        'qs': qs,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form
    }
    return render(request, 'posts/main.html', context)




@login_required
def liked_unliked_view(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST['post_id']
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)
        post_obj.save()
        
        like, created = Like.objects.get_or_create(user=profile, post=post_obj)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'
        like.save()

    return redirect('posts:main-post-view')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:main-post-view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You need to be the author of the post in order to delete it')
        return obj

class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:main-post-view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'You need to be the author of the post in order to updated it')
            return super().form_invalid(form)


