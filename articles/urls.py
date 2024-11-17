from django.urls import path
from .views import (
    ArticleListCreateView, ArticleDetailView, CategoryListView,
    LikeArticleView, ChangePasswordView, CommentListCreateView
)

urlpatterns = [
    path('articles/', ArticleListCreateView.as_view(), name='article-list-create'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('articles/<int:pk>/like/', LikeArticleView.as_view(), name='like-article'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('articles/<int:article_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),

]
