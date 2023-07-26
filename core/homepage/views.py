import urllib.parse

from datetime import timedelta, datetime, date


from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.db import transaction as db_transaction
from django.db.models import Q, F, Count, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status, serializers
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

from accounts.models import Account
from accounts.serializers import AccountSubSerializer
from homepage.models import Transaction, Properties, Comments, Hashtag, UserReaction, Reaction
from homepage.paginations import CustomPagination, PaginationHandlerMixin
from homepage.serializers import PropertiesSerializer, PropertiesSubSerializer, CommentsSerializer, TransactionSerializer,\
    UserReactionWithUserInfoSerializer, UserReactionSerializer
from homepage.utils import get_current_month_year, get_quaterly_dates, get_last_six_month


class Index(generics.ListCreateAPIView):
    queryset = Transaction.objects.filter(active=True, parent=None)
    serializer_class =  TransactionSerializer


class Comment(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class CommentApi(APIView):
    def get(self, request):
        comment = request.user
        serializer = CommentsSerializer(comment, many=False)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        idd = request.data.get("id", None)
        if not idd:
            raise serializers.ValidationError({"id": "id is required."})
        transaction_data = get_object_or_404(Transaction, id=idd)
        serializer = CommentsSerializer(instance=transaction_data, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "status": "Success",
                    "code": 200,
                    "message": "Successfully updated react data.",
                    "response": serializer.data,
                }, status=status.HTTP_200_OK
            )
        return Response(
            {
                "status": "Error",
                "message": "Serializer validation error.",
                "response": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST
        )


class Property(generics.ListCreateAPIView):
    queryset = Properties.objects.all()
    serializer_class = PropertiesSerializer


class PropertySub(generics.ListCreateAPIView):
    queryset = Properties.objects.all()
    serializer_class = PropertiesSubSerializer


class TodayEventView(APIView):
    def get(self, request):
        today = date.today()
        users = Account.objects.filter(Q(birth_date__month=today.month, birth_date__day=today.day) |
                                       Q(hire_date__month=today.month, hire_date__day=today.day))
        serializer = AccountSubSerializer(users, many=True)
        return Response(serializer.data)


class TopEmployees(APIView):
    def get(self, request):
        thirty_days_ago = timezone.now() - timedelta(days=30)

        # Count the number of times each recipient received points
        recipient_counts = Transaction.objects.filter(
            created__gte=thirty_days_ago
        ).values('recipients').annotate(
            count=Count('recipients')
        ).order_by('-count')[:5]

        top_employees = []
        for count_data in recipient_counts:
            recipient_id = count_data['recipients']
            count = count_data['count']
            recipient = Account.objects.get(pk=recipient_id)
            top_employees.append({'recipient': recipient.full_name,
                                  'count': count,
                                  'avtar': recipient.avtar.url,
                                  'id': recipient.id}
                                 )

        return Response(top_employees)


#@authentication_classes([JWTAuthentication])
class TransactionView(APIView, PaginationHandlerMixin):
    pagination_class = CustomPagination
    parser_classes = (MultiPartParser, FormParser)
    #permission_classes = [IsAuthenticated]

    def _filter_by_datetime(self, queryset, date_range):
        if date_range == "all":
            return queryset

        elif date_range == "this_month":
            this_month, this_year = get_current_month_year("this_month")
            return queryset.filter(created__month=this_month, created__year=this_year)

        elif date_range == "last_month":
            p_month, p_year = get_current_month_year("last_month")
            return queryset.filter(created__month=p_month, created__year=p_year)

        elif date_range == "this_quarter":
            first_date, last_date = get_quaterly_dates("this_quarter")
            return queryset.filter(created__range=[first_date, last_date])

        elif date_range == "last_quarter":
            first_date, last_date = get_quaterly_dates("last_quarter")
            return queryset.filter(created__range=[first_date, last_date])

        elif date_range == "last_six_month":
            last_six_month_date, current_date = get_last_six_month()
            return queryset.filter(created__range=[last_six_month_date, current_date])

        elif date_range == "year_to_date":
            current_date = datetime.now()
            current_year = current_date.year
            first_date = f"{current_year}-01-01"
            return queryset.filter(created__range=[first_date, current_date])


    def get(self, request):
        current_user_id = request.user.id
        parent_transactions = Transaction.objects\
            .filter(active=True, parent=None)\
            .prefetch_related(
                'recipients',
                'children',
                'hashtags',
            ).select_related(
                'sender',
                'created_by',
                'updated_by',
            )

        # Get query params from the get request
        sender_id = self.request.GET.get('sender', None)
        recipients_ids = self.request.GET.get('recipients', None)
        pagination = self.request.GET.get('pagination', None)
        date_range = request.GET.get("date_range", None)
        key_param = self.request.GET.get('key_param', None)
        hashtags_param = request.GET.get('hashtags', None)

        # Filter by date range
        if date_range:
            parent_transactions = self._filter_by_datetime(parent_transactions, date_range)
        
        # Filter by sender
        if sender_id:
            parent_transactions = parent_transactions\
                .filter(sender__id=sender_id)

        # Filter by recipeints
        if recipients_ids:
            recipients_ids_list = recipients_ids.split(',')
            parent_transactions = parent_transactions\
                .filter(recipients__id__in=recipients_ids_list)
        
        # Filter by key_params
        if key_param:
            if key_param == "popular":
                # We are using annotate and Coalesce function to calculate the sum of 
                # children and parent's points and add it to a new queryset 
                # field total_points.
                parent_transactions = parent_transactions\
                    .annotate(
                        total_points=F('point') + Coalesce(Sum('children__point'), 0)
                    )\
                    .order_by('-total_points')
            elif key_param == 'relevant':
                parent_transactions = parent_transactions\
                    .filter(
                    Q(sender__id=current_user_id) | 
                    Q(recipients__id=current_user_id)
                )

        # Filter by hashtags
        if hashtags_param:
            hashtags_names = hashtags_param.split(',')

            parent_transactions = parent_transactions\
                .filter(hashtags__name__in=hashtags_names)

        # Pagination
        if pagination:
            parent_transactions = self.paginate_queryset(parent_transactions)
        
        response_data = TransactionSerializer(parent_transactions, many=True).data
        return Response(response_data)


    def post(self, request):
        sender_id = request.data.get('sender')
        recipients_ids = request.data.get('recipients').split(",")
        point = int(request.data.get('point', 0))
        hashtags_names = request.data.get('hashtags').split(",")
        parent_id = request.data.get('parent_id', None)
        parent_transaction = None

        if parent_id:
            # Try to get the parent Transaction object
            parent_transaction = Transaction.objects.filter(id=parent_id).first()
            if not parent_transaction:
                return Response({'message': 'Parent Transaction not found.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the sender and check if it exists
        sender = get_object_or_404(Account, id=sender_id)

        # Check if sender has enough points
        if sender.points_available < point:
            return Response({'message': 'Insufficient points available.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if recipients are specified
        if not recipients_ids:
            return Response({'message': 'No recipients specified.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TransactionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Update the related fields of the transaction manually
            transaction = serializer.save(sender=sender)
            transaction.recipients.set(recipients_ids)

            if parent_transaction:
                transaction.parent = parent_transaction

            for hashtag in hashtags_names:
                db_hashtag = get_object_or_404(Hashtag, name=hashtag)   
                transaction.hashtags.add(db_hashtag)

            transaction.save()

            try:
                with db_transaction.atomic():
                    recipients_to_update = Account.objects\
                        .filter(id__in=recipients_ids)\
                        .update(points_received=F('points_received') + 10)

                    sender.points_available -= (point * len(recipients_ids))
                    sender.save()

            except Exception as e:
                # Handle any exceptions during the transaction
                return Response({'message': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Return the serialized data of the created Transaction object
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Return serializer errors if data is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

    def patch(self, request):
        id = request.data.get("id", None)

        if not id:
            raise serializers.ValidationError({"id": "id is required."})
        
        transaction_data = get_object_or_404(Transaction, id=id)

        serializer = TransactionSerializer(instance=transaction_data, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "status": "Success",
                    "code": 200,
                    "message": "Successfully updated react data.",
                    "response": serializer.data,
                }, status=status.HTTP_200_OK
            )
        return Response(
            {
                "status": "Error",
                "message": "Serializer validation error.",
                "response": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST
        )


class PointsTransferListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.filter(active=True)
    serializer_class = TransactionSerializer

    @db_transaction.atomic
    def perform_create(self, serializer):
        sender = self.request.user
        receivers_data = self.request.data.get('receivers', [])

        total_points = int(self.request.data.get('points_available', 0))

        num_receivers = len(receivers_data)
        points_per_receiver = total_points // num_receivers
        remaining_points = total_points % num_receivers

        transfer = serializer.save(sender=sender, points_available=total_points)

        for receiver_data in receivers_data:
            receiver_id = receiver_data.get('id')
            receiver = Account.objects.get(id=receiver_id)

            points_to_receive = points_per_receiver
            if remaining_points > 0:
                points_to_receive += 1
                remaining_points -= 1

            receiver.points_received += points_to_receive
            receiver.save()

            transfer.receivers.add(receiver)

        sender.points_available -= total_points
        sender.save()

@authentication_classes([JWTAuthentication])
class AddUserReactionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserReactionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            reaction_hash = serializer.initial_data.get('reaction_hash')
            content_type_name = serializer.initial_data.get('content_type')
            object_id = serializer.validated_data.get('object_id')

            try:
                reaction = Reaction.objects.get(reaction_hash=reaction_hash)
            except Reaction.DoesNotExist:
                return Response({'detail': 'Invalid reaction_hash.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if content_type_name.lower() in ['transaction', 'comments']:
                content_type = ContentType.objects.get(model=content_type_name)

            # Set the authenticated user as the creator
            serializer.save(reaction=reaction, content_type=content_type, object_id=object_id, created_by=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@authentication_classes([JWTAuthentication])
class TransactionReactionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, transaction_id, reaction_hash=None, format=None):
        reactions = UserReaction.objects\
            .select_related('reaction', 'created_by', 'updated_by')\
            .prefetch_related('content_type')\
            .filter(
            content_type__model='transaction', 
            object_id=transaction_id
        )

        if reaction_hash:
            reactions = reactions.filter(reaction__reaction_hash=reaction_hash)

        serializer = UserReactionWithUserInfoSerializer(reactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# OLD CODE 
"""@authentication_classes([JWTAuthentication])
class Transaction(APIView, PaginationHandlerMixin):
    pagination_class = CustomPagination
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def calculate_point(self, point, id):
        points = [i.point for i in Posts.objects.filter(parent_id=id)]
        return point + sum(points)

    def _filter_by_datetime(self, date_range=None):
        if date_range == "all":
            return Posts.objects.all()

        elif date_range == "this_month":
            this_month, this_year = get_current_month_year("this_month")
            return Posts.objects.filter(created__month=this_month, created__year=this_year)

        elif date_range == "last_month":
            p_month, p_year = get_current_month_year("last_month")
            return Posts.objects.filter(created__month=p_month, created__year=p_year)

        elif date_range == "this_quarter":
            first_date, last_date = get_quaterly_dates("this_quarter")
            return Posts.objects.filter(created__range=[first_date, last_date])

        elif date_range == "last_quarter":
            first_date, last_date = get_quaterly_dates("last_quarter")
            return Posts.objects.filter(created__range=[first_date, last_date])

        elif date_range == "last_six_month":
            last_six_month_date, current_date = get_last_six_month()
            return Posts.objects.filter(created__range=[last_six_month_date, current_date])

        elif date_range == "year_to_date":
            current_date = datetime.now()
            current_year = current_date.year
            first_date = f"{current_year}-01-01"
            return Posts.objects.filter(created__range=[first_date, current_date])

    def get(self, request):
        user = request.user
        print(user.id)
        sender = self.request.GET.get('sender', None)
        recipients = self.request.GET.get('recipients', None)
        pagination = self.request.GET.get('pagination', None)

        # date_range all, this_month, last_month, this_quarter, last_quarter, year_to_date, last_six_month
        date_range = request.GET.get("date_range", None)

        # key_param all, popular, relevant
        key_param = self.request.GET.get('key_param', None)

        if date_range:
            transaction_queryset = self._filter_by_datetime(date_range)

        elif sender or recipients:
            if sender:
                transaction_queryset = Posts.objects.filter(sender=sender)
            if recipients:
                transaction_queryset = Posts.objects.filter(recipients=recipients)

        elif key_param:
            if key_param == 'popular':
                transaction_queryset = Posts.objects.filter(parent_id=None, active=True)
                popular_list = []
                for instance in transaction_queryset:
                    popular_list.append({
                        "id": instance.id,
                        "parent_id": instance.parent_id,
                        "point": instance.point,
                        "recipients": instance.recipients,
                        "sender": instance.sender,
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
                        "points": self.calculate_point(instance.point, instance.id)
                    })
                from operator import itemgetter
                transaction_queryset = sorted(popular_list, key=itemgetter('points'), reverse=True)

            elif key_param == 'relevant':
                transaction_queryset = Posts.objects.filter(Q(sender=user.id) | Q(recipients=user.id))

            elif key_param == 'all':
                transaction_queryset = Posts.objects.all()

        else:
            transaction_queryset = Posts.objects.all()

        transaction_queryset.prefetch_related('recipients').select_related('sender')

        if pagination:
            page = self.paginate_queryset(transaction_queryset)
            serializer = PostSerializer(page, many=True)
            return Response(self.get_paginated_response(serializer.data).data)

        serializer = PostSerializer(transaction_queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        idd = request.data.get("id", None)
        if not idd:
            raise serializers.ValidationError({"id": "id is required."})
        transaction_data = get_object_or_404(Posts, id=idd)
        serializer = PostSerializer(instance=transaction_data, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "status": "Success",
                    "code": 200,
                    "message": "Successfully updated react data.",
                    "response": serializer.data,
                }, status=status.HTTP_200_OK
            )
        return Response(
            {
                "status": "Error",
                "message": "Serializer validation error.",
                "response": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST
        )"""
