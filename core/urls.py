from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from booksocial.views import (
    CustomTokenObtainPairView, UserRegisterView, ProfileView,
    BookListView, BookDetailView, ReviewCreateView,
    ReadingListView, FollowUserView
)


# Стартовая страница
def home(request):
    return HttpResponse("Добро пожаловать в BookStore API!")


# Редирект на /api/books/
def home_redirect(request):
    return redirect('book-list')


urlpatterns = [
    path('admin/', admin.site.urls),

    # Маршруты авторизации
    path('api/auth/register/', UserRegisterView.as_view(), name='register'),
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Профиль пользователя
    path('api/profile/', ProfileView.as_view(), name='profile'),

    # Книги
    path('api/books/', BookListView.as_view(), name='book-list'),
    path('api/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    # Ревью
    path('api/reviews/', ReviewCreateView.as_view(), name='review-create'),

    # Списки книг
    path('api/lists/', ReadingListView.as_view(), name='reading-list'),

    # Подписка на пользователей
    path('api/follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),

    # Стартовая страница (для корня)
    path('', home_redirect),  # Или можно использовать home(), если просто текст показывать

    # Swagger UI и OpenAPI схема
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
