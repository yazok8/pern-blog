from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet, CategoryViewSet, TagViewSet, PostViewSet, 
    ArticleViewSet, CommentViewSet, SiteSettingsViewSet
)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)
router.register('tags', TagViewSet)
router.register('posts', PostViewSet, basename='post')
router.register('articles', ArticleViewSet, basename='article')
router.register('comments', CommentViewSet)
router.register('settings', SiteSettingsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
