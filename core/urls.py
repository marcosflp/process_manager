from django.urls import path, include

from core.views import (
    HomeView, ProfileListView, ProfileCreateView,
    ProfileUpdateView, ProfileDeleteView
)

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('', HomeView.as_view(), name='home'),

    path('profile/', ProfileListView.as_view(), name='profile-list-view'),
    path('profile/create/', ProfileCreateView.as_view(), name='profile-create-view'),
    path('profile/update/<int:pk>/', ProfileUpdateView.as_view(), name='profile-update-view'),
    path('profile/delete/<int:pk>/', ProfileDeleteView.as_view(), name='profile-delete-view'),
]
