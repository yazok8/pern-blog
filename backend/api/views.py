from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from accounts.models import User
from content.models import Category, Tag, Post, Article, Comment, Like, ArticleLike
from settings.models import SiteSettings
from .serializers import (
    UserSerializer, CategorySerializer, TagSerializer, PostSerializer, 
    ArticleSerializer, CommentSerializer, LikeSerializer, ArticleLikeSerializer,
    SiteSettingsSerializer
)
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly, IsOwnerOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug']
    lookup_field = 'slug'

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug']
    lookup_field = 'slug'

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['published', 'author', 'categories', 'tags', 'content_type']
    search_fields = ['title', 'content', 'excerpt']
    lookup_field = 'slug'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.all()
        elif self.request.user.is_authenticated:
            # Authors can see their own unpublished posts
            return Post.objects.filter(
                published=True
            ) | Post.objects.filter(author=self.request.user)
        else:
            # Anonymous users can only see published posts
            return Post.objects.filter(published=True)
    
    @action(detail=True, methods=['post'])
    def like(self, request, slug=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if created:
            return Response({'status': 'post liked'})
        else:
            like.delete()
            return Response({'status': 'post unliked'})
    
    @action(detail=True, methods=['post'])
    def view(self, request, slug=None):
        post = self.get_object()
        post.views += 1
        post.save()
        return Response({'status': 'view counted'})

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['published', 'author', 'categories', 'tags', 'type', 'is_featured', 'is_sponsored']
    search_fields = ['title', 'content', 'excerpt']
    lookup_field = 'slug'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Article.objects.all()
        elif self.request.user.is_authenticated:
            # Authors can see their own unpublished articles
            return Article.objects.filter(
                published=True
            ) | Article.objects.filter(author=self.request.user)
        else:
            # Anonymous users can only see published articles
            return Article.objects.filter(published=True)
    
    @action(detail=True, methods=['post'])
    def like(self, request, slug=None):
        article = self.get_object()
        like, created = ArticleLike.objects.get_or_create(article=article, user=request.user)
        if created:
            return Response({'status': 'article liked'})
        else:
            like.delete()
            return Response({'status': 'article unliked'})
    
    @action(detail=True, methods=['post'])
    def view(self, request, slug=None):
        article = self.get_object()
        article.views += 1
        article.save()
        return Response({'status': 'view counted'})

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'article', 'author', 'parent']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class SiteSettingsViewSet(viewsets.ModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        settings = SiteSettings.objects.first()
        if not settings:
            settings = SiteSettings.objects.create(site_name="My Blog")
        serializer = self.get_serializer(settings)
        return Response(serializer.data)
