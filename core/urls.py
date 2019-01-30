from django.urls import path, include

from core.views import HomeView

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('', HomeView.as_view(), name='home')
]
