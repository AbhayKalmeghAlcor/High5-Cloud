from rest_framework import serializers
from .models import Posts, Comments, Company, Properties, Recognition
from accounts.models import Account
from accounts.serializers import AccountSubSerializer
from django.core.exceptions import ValidationError


def validate_image_size(image):
    # Maximum allowed file size in bytes (e.g., 2MB)
    max_size = 3 * 1024 * 1024

    if image.size > max_size:
        raise ValidationError(f"The maximum file size allowed is {max_size} bytes.")


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id', 'parent_id', 'point', 'recipients', 'sender', 'message', 'hashtags', 'image', 'gif', 'link',
                  'active', 'flag_transaction', 'react_by', 'created_by', 'created', 'updated_by', 'updated']

    def to_representation(self, instance):
        response_data = super().to_representation(instance)
        recipients_data = response_data.get('recipients', [])
        recipients = Account.objects.filter(id__in=recipients_data)
        recipients_serializer = AccountSubSerializer(recipients, many=True)
        # recipients_serializer_sender = AccountSubSerializer(sender,)
        response_data['recipients'] = recipients_serializer.data
        response_data['sender'] = AccountSubSerializer(
            Account.objects.filter(
                id=response_data.get('sender')), many=True
        ).data
        return response_data

    def validate_image(self, image):
        # Check if the image size is more than 2MB (2 * 1024 * 1024 bytes)
        if image.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Image size should not exceed 2MB.")
        return image


    # def get_recipients_data(self, obj):
    #     recipients_serializer = AccountSubSerializer(obj.recipients)
    #     return recipients_serializer.data


class PropertiesSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    hashtage = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
        default=[
            "#OneTeam", "#Vision", "#Collaboration", "#Culture",
            "#Training", "#Quality", "#ProblemSolving", "#Teambuilding"
        ]
    )

    points_range = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
        default=[10, 20, 30, 40, 50])

    class Meta:
        model = Properties
        fields = ['hashtage', 'points_range', 'monthly_allowance', 'birthday_points', 'anniversary_points',
                  'created', 'updated', 'active', 'company']

    def get_company_data(self, obj):
        company_serializer = CompanySerializer(obj.company)
        return company_serializer.data


class PropertiesSubSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = Properties
        fields = '__all__'


class RecognitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recognition
        fields = '__all__'
