from rest_framework.serializers import ModelSerializer
from .models import Post, Comment, Like

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        exclude = ['created_at', 'updated_at', 'author']  # Exclude created_at, updated_at, and author fields from the Post model

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['created_at']  # Exclude created_at, author, and post fields from the Comment model
        extra_kwargs = {'post': {'read_only': True}, 
                        'author': {'read_only': True}}

class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ['post', 'user']
        extra_kwargs = {'post': {'read_only': True}, 
                        'user': {'read_only': True}}