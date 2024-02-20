from django.urls import path
from .views import GlassdoorView

urlpatterns = [
    path('home', GlassdoorView.as_view()),
]
