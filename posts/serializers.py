from rest_framework import serializers

from users.models import User as user_model
from . import models


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comments
        fields = (
            'id',
            'contents',
        )


class FeedAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = (
            'id',
            'username',
            'profile_photo',
        )


class PostSerializer(serializers.ModelSerializer):
    comment_post = CommentSerializer(many=True)
    author = FeedAuthorSerializer()
    class Meta:
        model = models.Post # 포스트에서 필드들을 추출
        fields = (
            'id', 
            'image', 
            'caption', 
            'comment_post',
            'author',
            )
