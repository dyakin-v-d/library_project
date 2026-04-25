from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, CategoryViewSet

router = DefaultRouter()

# Теперь список книг будет доступен по пустому пути (относительно этого файла)
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
]