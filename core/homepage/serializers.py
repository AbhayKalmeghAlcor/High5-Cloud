from rest_framework import serializers
from .models import Posts, Company, Properties, Recognition,Comments
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
                  'active', 'flag_transaction', 'react_by', 'created_by', 'created', 'updated_by']

    def to_representation(self, instance):
        try:
            return {
                "id": instance.id,
                "parent_id": instance.parent_id,
                "point": instance.point,
                "recipients": [{
                    "id": val.id,
                    "first_name": val.first_name,
                    "last_name": val.last_name,
                    "email": val.email,
                    "phone_number": val.phone_number,
                    "interest": val.interest,
                    "points_available": val.points_available,
                    "points_received": val.points_received,
                    "points_redeemed": val.points_redeemed,
                    "birth_date": val.birth_date,
                    "hire_date": val.hire_date,
                    "avtar": val.avtar.url,
                    "location": val.location,
                    "title": val.title,
                    "department": val.department,
                    "created_date": val.created_date,
                    "updated_date": val.updated_date,
                    "full_name": val.full_name,
                    "react": val.react
                } for val in instance.recipients.all()],
                "sender": [{
                    "id": instance.sender.id,
                    "first_name":  instance.sender.first_name,
                    "last_name":  instance.sender.last_name,
                    "email":  instance.sender.email,
                    "phone_number":  instance.sender.phone_number,
                    "interest":  instance.sender.interest,
                    "points_available":  instance.sender.points_available,
                    "points_received":  instance.sender.points_received,
                    "points_redeemed":  instance.sender.points_redeemed,
                    "birth_date":  instance.sender.birth_date,
                    "hire_date":  instance.sender.hire_date,
                    "avtar":  instance.sender.avtar.url,
                    "location":  instance.sender.location,
                    "title":  instance.sender.title,
                    "department":  instance.sender.department,
                    "created_date":  instance.sender.created_date,
                    "updated_date":  instance.sender.updated_date,
                    "full_name":  instance.sender.full_name,
                    "react":  instance.sender.react
                }],
                "message": instance.message,
                "hashtags": instance.hashtags,
                "image": instance.image.url if instance.image else None,
                "gif": instance.gif,
                "link": instance.link,
                "active": instance.active,
                "flag_transaction": instance.flag_transaction,
                "react_by": instance.react_by,
                "created_by": instance.created_by.id,
                "created": instance.created,
                "updated_by": instance.updated_by.id,
                # "points": instance.points
            }
        except:
            return {
                "id": instance['id'],
                "parent_id": instance['parent_id'],
                "point": instance['point'],
                "recipients": [{
                    "id": val.id,
                    "first_name": val.first_name,
                    "last_name": val.last_name,
                    "email": val.email,
                    "phone_number": val.phone_number,
                    "interest": val.interest,
                    "points_available": val.points_available,
                    "points_received": val.points_received,
                    "points_redeemed": val.points_redeemed,
                    "birth_date": val.birth_date,
                    "hire_date": val.hire_date,
                    "avtar": val.avtar.url,
                    "location": val.location,
                    "title": val.title,
                    "department": val.department,
                    "created_date": val.created_date,
                    "updated_date": val.updated_date,
                    "full_name": val.full_name,
                    "react": val.react
                } for val in instance['recipients'].all()],
                "sender": [{
                    "id": instance['sender'].id,
                    "first_name": instance['sender'].first_name,
                    "last_name": instance['sender'].last_name,
                    "email": instance['sender'].email,
                    "phone_number": instance['sender'].phone_number,
                    "interest": instance['sender'].interest,
                    "points_available": instance['sender'].points_available,
                    "points_received": instance['sender'].points_received,
                    "points_redeemed": instance['sender'].points_redeemed,
                    "birth_date": instance['sender'].birth_date,
                    "hire_date": instance['sender'].hire_date,
                    "avtar": instance['sender'].avtar.url,
                    "location": instance['sender'].location,
                    "title": instance['sender'].title,
                    "department": instance['sender'].department,
                    "created_date": instance['sender'].created_date,
                    "updated_date": instance['sender'].updated_date,
                    "full_name": instance['sender'].full_name,
                    "react": instance['sender'].react,
                }],
                "message": instance['message'],
                "hashtags": instance['hashtags'],
                "image": instance['image'].url if instance['image'] else None,
                "gif": instance['gif'],
                "link": instance['link'],
                "active": instance['active'],
                "flag_transaction": instance['flag_transaction'],
                "react_by": instance['react_by'],
                "created_by": str(instance['created_by']),
                "created": instance['created'],
                "updated_by": str(instance['updated_by']),
                "points": instance['points']
            }


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
