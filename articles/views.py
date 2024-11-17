from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from django.contrib.auth.models import User
from .models import Article, Category, Like, Comment
from .serializers import ArticleSerializer, CategorySerializer, UserSerializer, CommentSerializer
from django.contrib.auth import update_session_auth_hash
from rest_framework_simplejwt.tokens import RefreshToken


# CRUD для статей
class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']


# Категории
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Лайки для статей
class LikeArticleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        Like.objects.get_or_create(user=request.user, article=article)
        return Response({'status': 'liked'})


# Изменение пароля
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        new_password = request.data.get('new_password')
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        return Response({'status': 'password changed'})


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        article_id = self.kwargs['article_id']
        return Comment.objects.filter(article_id=article_id)

    def perform_create(self, serializer):
        article_id = self.kwargs['article_id']
        serializer.save(user=self.request.user, article_id=article_id)

