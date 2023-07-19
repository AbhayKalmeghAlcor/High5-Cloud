from .models import Posts, Properties, Comments
from .serializers import PostSerializer, PropertiesSerializer, PropertiesSubSerializer, CommentsSerializer
from rest_framework import generics
from django.db.models import Q
from accounts.models import Account
from accounts.serializers import AccountSubSerializer
from django.utils import timezone
from datetime import timedelta, datetime, date
from django.db.models import Count
from .paginations import CustomPagination, PaginationHandlerMixin
from .utils import get_current_month_year, get_quaterly_dates, get_last_six_month
from django.db import transaction
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, serializers
from django.shortcuts import get_object_or_404
from django.db.models import F


class Index(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer


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
        transaction_data = get_object_or_404(Posts, id=idd)
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
        recipient_counts = Posts.objects.filter(
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


@authentication_classes([JWTAuthentication])
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
                transaction_queryset = Posts.objects.filter(parent_id=None)
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
        )


class PointsTransferListCreateView(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    @transaction.atomic
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
