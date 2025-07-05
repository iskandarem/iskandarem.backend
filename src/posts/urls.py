from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, LikeViewSet


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

# Register nested routes for comments and likes
posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')
posts_router.register(r'likes', LikeViewSet, basename='post-likes')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
]