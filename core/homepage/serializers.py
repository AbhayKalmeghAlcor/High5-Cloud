from rest_framework import serializers
from .models import Posts, Comments


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    comment = CommentSerializer()

    class Meta:
        model = Posts
        fields = ['point', 'recipients', 'sender', 'hashtags', 'image', 'gif', 'link', 'active',
                  'flag_transaction', 'created', 'react_by', 'created_by', 'updated', 'comment']

    def get_comments_data(self, obj):
        comment_serializer = CommentSerializer(obj.comment)
        return comment_serializer.data
