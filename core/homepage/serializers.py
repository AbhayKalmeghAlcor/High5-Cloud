from rest_framework import serializers
from .models import Posts, Comments, Company, Properties


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
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


class PropertiesSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = Properties
        fields = ['hashtags', 'monthly_allowance', 'points_given', 'birthday_points', 'anniversary_points', 'company']

    def get_company_data(self, obj):
        company_serializer = CompanySerializer(obj.company)
        return company_serializer.data
