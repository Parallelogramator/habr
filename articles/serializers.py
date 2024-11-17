from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article, Category, Like, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'

    def get_likes_count(self, obj):
        return obj.like_set.count()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'article']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'article', 'content', 'created_at']
