from django.core.exceptions import ValidationError
from rest_framework import serializers

from accounts.models import Account
from accounts.serializers import AccountSubSerializer
from homepage.models import Company, Properties, Comments, Transaction, Hashtag


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


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['name']


class TransactionSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField('get_children')
    recipients = AccountSubSerializer(many=True, read_only=True)
    sender = AccountSubSerializer(read_only=True)
    created_by = AccountSubSerializer(read_only=True)
    updated_by = AccountSubSerializer(read_only=True)
    hashtags = HashtagSerializer(read_only=True, many=True)

    def get_children(self, transaction):
        children = Transaction.objects.filter(parent=transaction, active=True)
        serializer = TransactionSerializer(children, many=True)
        return serializer.data

    class Meta:
        model = Transaction
        fields = ['id', 'children', 'point', 'recipients', 'sender', 'message', 
                  'hashtags', 'image', 'gif', 'link', 'active', 'flag_transaction', 
                  'react_by', 'created_by', 'created', 'updated_by']
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['updated_by'] = request.user
        return super().update(instance, validated_data)


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
