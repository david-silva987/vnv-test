from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'note'

router = DefaultRouter()
router.register(r'notes', views.NoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]