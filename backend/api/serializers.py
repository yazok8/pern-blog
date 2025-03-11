from rest_framework import serializers
from accounts.models import User
from content.models import Category, Tag, Post, Article, Comment, Like, ArticleLike
from settings.models import SiteSettings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'bio', 'profile_image', 'role', 'created_at']
        read_only_fields = ['created_at']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'post', 'article', 'author', 'author_name', 'parent', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'published', 
            'featured_image', 'author', 'author_name', 'categories', 'tags', 
            'created_at', 'updated_at', 'views', 'reading_time', 'content_type',
            'comments_count', 'likes_count'
        ]
        read_only_fields = ['created_at', 'updated_at', 'views']

class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'published', 
            'featured_image', 'author', 'author_name', 'categories', 'tags', 
            'created_at', 'updated_at', 'views', 'reading_time', 'type',
            'is_sponsored', 'is_featured', 'seo_meta', 'references', 'cover_design',
            'comments_count', 'likes_count'
        ]
        read_only_fields = ['created_at', 'updated_at', 'views']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['created_at']

class ArticleLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleLike
        fields = ['id', 'article', 'user', 'created_at']
        read_only_fields = ['created_at']

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        read_only_fields = ['updated_at']