from django.urls import path
from .views import GlassdoorListView, GlassdoorCreateView

urlpatterns = [
    path('get', GlassdoorListView.as_view()),
    path('create', GlassdoorCreateView.as_view()),
]
