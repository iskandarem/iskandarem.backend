from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import *

# Create your views here.
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthor]


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor, IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        post_id = self.kwargs['post_pk']  # 'post_pk' comes from lookup='post' in the router
        return Comment.objects.filter(post__id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_pk']
        serializer.save(author=self.request.user, post_id=post_id)

class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [LikePermission]

    def get_queryset(self):
        post_id = self.kwargs['post_pk']  # 'post_pk' comes from lookup='post' in the router
        return Like.objects.filter(post__id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_pk']
        serializer.save(user=self.request.user, post_id=post_id)
