from rest_framework import serializers

from accounts.models import Account
from accounts.serializers import AccountSubSerializer
from homepage.models import Company, Properties, Comment, Transaction, Hashtag, Reaction, UserReaction


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'


class UserReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReaction
        exclude = ('reaction', 'content_type', 'created_by')


class UserReactionWithUserInfoSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()
    user_role = serializers.SerializerMethodField()
    user_department = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()
    reaction = serializers.SerializerMethodField()

    class Meta:
        model = UserReaction
        fields = ('reaction', 'content_type', 'object_id', 'user_full_name', 'user_role', 'user_department')

    def get_user_full_name(self, obj):
        return obj.created_by.get_full_name()

    def get_user_role(self, obj):
        return obj.created_by.role

    def get_user_department(self, obj):
        return obj.created_by.department

    def get_content_type(self, obj):
        return obj.content_type.model
    
    def get_reaction(self, obj):
        return obj.reaction.reaction_hash

class UpdateUserReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReaction
        fields = ('reaction',)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['name']


class CommentSerializer(serializers.ModelSerializer):
    reaction_hashes = serializers.SerializerMethodField()
    total_reaction_counts = serializers.SerializerMethodField()
    created_by = AccountSubSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'comment', 'image', 'gif', 'reaction_hashes',
            'total_reaction_counts', 'created_by', 'created', 'updated'
        )

    def get_reaction_hashes(self, obj):
        reactions = UserReaction.objects\
            .filter(content_type__model='comment', object_id=obj.id)\
            .values_list('reaction__reaction_hash', flat=True)

        return list(reactions)


    def get_total_reaction_counts(self, obj):
        return UserReaction.objects\
            .filter(content_type__model='comment', object_id=obj.id)\
            .count()


class ChildTransactionSerializer(serializers.ModelSerializer):
    recipients = AccountSubSerializer(many=True, read_only=True)
    sender = AccountSubSerializer(read_only=True)
    hashtags = HashtagSerializer(read_only=True, many=True)
    comments = CommentSerializer(many=True, read_only=True)
    user_reaction_info = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            'id', 'point', 'recipients', 'sender', 'message', 'hashtags', 'image', 
            'gif', 'link', 'active', 'flag_transaction', 'created', 'comments', 'user_reaction_info'
        ]

    def get_user_reaction_info(self, instance):
        queryset = UserReaction.objects\
            .filter(content_type__model='transaction', object_id=instance.id)
        count = queryset.count()
        reaction_hashes = queryset\
            .values_list('reaction__reaction_hash', flat=True)
        
        return {
            'reaction_hashes': list(reaction_hashes),
            'total_reaction_count': count
        }


class TransactionSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField('get_children')
    recipients = AccountSubSerializer(many=True, read_only=True)
    sender = AccountSubSerializer(read_only=True)
    created_by = AccountSubSerializer(read_only=True)
    updated_by = AccountSubSerializer(read_only=True)
    hashtags = HashtagSerializer(read_only=True, many=True)
    comments = CommentSerializer(many=True, read_only=True)
    user_reaction_info = serializers.SerializerMethodField(read_only=True)

    def get_user_reaction_info(self, instance):
        user_full_name = None
        if not instance.created:
            if instance.latest_user_reaction_first_name:
                user_full_name = instance.latest_user_reaction_first_name
            if instance.latest_user_reaction_last_name:
                user_full_name += " " + instance.latest_user_reaction_last_name

            return {
                'latest_user_reaction_full_name': user_full_name,
                'reaction_hashes': instance.reaction_hashes,
                'total_reaction_counts': instance.total_reaction_counts,
                'is_reacted': instance.is_reacted,
            }
        else:
            return "not available"

    def get_children(self, transaction):
        children = Transaction.objects.filter(parent=transaction, active=True)
        serializer = ChildTransactionSerializer(children, many=True)
        return serializer.data

    class Meta:
        model = Transaction
        fields = [
            'id', 'children', 'point', 'recipients', 'sender', 'message', 'hashtags', 'image', 
            'gif', 'link', 'active', 'flag_transaction', 'created_by', 'created', 
            'updated_by', 'comments', 'user_reaction_info'
        ]
    
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
