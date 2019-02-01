from django.urls import path, include

from core.views import (
    HomeView,
    ProfileListView, ProfileCreateView, ProfileUpdateView, ProfileDeleteView,
    ProcessListView, ProcessCreateView, ProcessUpdateView, ProcessDeleteView,
    ProcessDetailView, ProcessFeedbackCreateView, ProcessFeedbackUpdateView,
    ProcessFeedbackDeleteView)

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('', HomeView.as_view(), name='home'),

    path('profile/',
         ProfileListView.as_view(),
         name='profile-list-view'),
    path('profile/create/',
         ProfileCreateView.as_view(),
         name='profile-create-view'),
    path('profile/update/<int:pk>/',
         ProfileUpdateView.as_view(),
         name='profile-update-view'),
    path('profile/delete/<int:pk>/',
         ProfileDeleteView.as_view(),
         name='profile-delete-view'),

    path('process/',
         ProcessListView.as_view(),
         name='process-list-view'),
    path('process/create/',
         ProcessCreateView.as_view(),
         name='process-create-view'),
    path('process/update/<int:pk>/',
         ProcessUpdateView.as_view(),
         name='process-update-view'),
    path('process/detail/<int:pk>/',
         ProcessDetailView.as_view(),
         name='process-detail-view'),
    path('process/delete/<int:pk>/',
         ProcessDeleteView.as_view(),
         name='process-delete-view'),

    path('process/<int:process_pk>/feedback/',
         ProcessFeedbackCreateView.as_view(),
         name='processfeedback-create-view'),
    path('process/<int:process_pk>/feedback/<int:pk>/',
         ProcessFeedbackUpdateView.as_view(),
         name='processfeedback-update-view'),
    path('process/<int:process_pk>/feedback/delete/<int:pk>/',
         ProcessFeedbackDeleteView.as_view(),
         name='processfeedback-delete-view'),
]
