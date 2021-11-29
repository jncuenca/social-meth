from django.shortcuts import render
from profiles.models import Profile
from django.http import HttpResponse


def home_view(request):

    context = {
        'user' : request.user,
        'hello': 'Hello world!'    
    }
    return render(request, 'main/home.html', context)

def search_user(request):
    user_search = request.GET.get('q')
    #user = ''.join(user_search.split())
    qs = Profile.objects.all()
    my_list  = list(filter(lambda x: (x.user.username == user_search), qs))
    
    profile = None
    is_empty = True

    if len(my_list) > 0:
        profile = my_list[0]
        is_empty = False
    

    context = {
        'is_empty' : is_empty, 
        'profile' : profile
    }
    
    return render(request, 'searched.html', context)

