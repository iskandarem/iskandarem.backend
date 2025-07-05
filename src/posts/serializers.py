from rest_framework.serializers import ModelSerializer
from .models import Post, Comment, Like

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        exclude = ['created_at', 'updated_at', 'author']  # Exclude created_at, updated_at, and author fields from the Post model

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['created_at', 'author', 'post']  # Exclude created_at, author, and post fields from the Comment model

class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        exclude = ['created_at', 'post']  # Exclude created_at and post fields from the Like model