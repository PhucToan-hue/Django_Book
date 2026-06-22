from django.urls import include, path
from rest_framework.routers import DefaultRouter

from book.views import BookViewSet, LogoutView

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
