from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Book, Review, ReadingList, Follow
from .serializers import (
    UserSerializer, BookSerializer, ReviewSerializer,
    ReadingListSerializer, FollowSerializer, CustomTokenObtainPairSerializer
)


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class BookListView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Добавляем возможность фильтрации
        queryset = Book.objects.all()
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author__icontains=author)
        return queryset


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        book_id = self.kwargs.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        serializer.save(user=self.request.user, book=book)


class ReadingListView(generics.ListCreateAPIView):
    serializer_class = ReadingListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Фильтрация по типу списка, если указан
        list_type = self.request.query_params.get('list_type')
        queryset = ReadingList.objects.filter(user=self.request.user)
        if list_type:
            queryset = queryset.filter(list_type=list_type)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FollowUserView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        following_id = kwargs.get('user_id')

        if request.user.id == following_id:
            return Response(
                {"error": "You cannot follow yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        following_user = get_object_or_404(User, id=following_id)

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=following_user
        )

        if not created:
            return Response(
                {"error": "You are already following this user"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
