from django.urls import path
from .views import (
    my_profile_view, 
    my_invites_view, 
    AllProfilesView,
    send_invatation, 
    remove_from_friends,
    accept_invitation,
    reject_invitation,
    ProfileDetailView,
)

app_name = 'profiles'

urlpatterns = [
    path('my-profile/', my_profile_view, name='my-profile'),
    path('my-invites/', my_invites_view, name='my-invites'),
    path('', AllProfilesView.as_view(), name='all-profiles'),
    path('send-invite/', send_invatation, name='send-invite'),
    path('remove-friend/', remove_from_friends, name='remove-friend'),
    path('my-invites/accept/', accept_invitation, name='accept-invite'),
    path('my-invites/reject/', reject_invitation, name='reject-invite'),
    path('<pk>/', ProfileDetailView.as_view(), name='profile-detail-view'),
]