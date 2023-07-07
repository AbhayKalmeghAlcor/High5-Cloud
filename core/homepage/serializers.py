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
    sender = AccountSubSerializer()
    image = serializers.ImageField(validators=[validate_image_size])

    # recipients = AccountSubSerializer()

    class Meta:
        model = Posts
        fields = ['id', 'parent_id', 'point', 'recipients', 'sender', 'message', 'hashtags', 'image', 'gif', 'link',
                  'active', 'flag_transaction', 'react_by', 'created_by', 'created', 'updated_by', 'updated']

    def get_sender_data(self, obj):
        sender_serializer = AccountSubSerializer(obj.sender)
        return sender_serializer.data

    def to_representation(self, instance):
        response_data = super().to_representation(instance)
        recipients_data = response_data.get('recipients', [])
        recipients = Account.objects.filter(id__in=recipients_data)
        recipients_serializer = AccountSubSerializer(recipients, many=True)
        response_data['recipients'] = recipients_serializer.data
        return response_data

    # def validate_image_size(self, image):
    #     # Adjust the desired image size here (in bytes)
    #     max_size = 3 * 1024 * 1024  # 2 MB
    #
    #     if image.size > max_size:
    #         raise serializers.ValidationError("Image size should not exceed 2 MB.")
    #     return image

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
