from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Posts
from django.db.models.signals import post_save

# @receiver(pre_save, sender=Posts)
# def update_sender_and_recipients_points(sender, instance, **kwargs):
#     # Calculate total points to be transferred
#     total_points = instance.point
#
#     # Deduct points from the sender's points_available field
#     instance.sender.points_available -= total_points
#     instance.sender.save()
#
#     # Calculate points to be transferred to each recipient
#     num_recipients = instance.recipients.count()
#     points_per_recipient = total_points // num_recipients
#     remaining_points = total_points % num_recipients
#
#     # Add points to the recipients' points_received field
#     for recipient in instance.recipients.all():
#         points_to_receive = points_per_recipient
#         if remaining_points > 0:
#             points_to_receive += 1
#             remaining_points -= 1
#
#         recipient.points_received += points_to_receive
#         recipient.save()
#
# #
# # @receiver(pre_save, sender=Posts)
# def update_sender_and_recipients_points(sender, instance, **kwargs):
#     total_points = instance.point
#     num_recipients = instance.recipients.count()
#     print(f"total_points {total_points}, num_recipients {num_recipients}")
#
#     if num_recipients > 0:
#         points_per_recipient = total_points // num_recipients
#         remaining_points = total_points % num_recipients
#
#         for recipient in instance.recipients.all():
#             points_to_receive = points_per_recipient
#             if remaining_points > 0:
#                 points_to_receive += 1
#                 remaining_points -= 1
#
#             recipient.points_received += points_to_receive
#             recipient.save()
#
#     instance.sender.points_available -= total_points
#     instance.sender.save()
#

#
# @receiver(pre_save, sender=Posts)
# def update_sender_and_recipients_points(sender, instance, **kwargs):
#     total_points = instance.point
#     num_recipients = instance.recipients.count()
#     print(f"total_points {total_points}, num_recipients {num_recipients}")
#
#     if num_recipients > 0:
#         points_per_recipient = total_points // num_recipients
#         remaining_points = total_points % num_recipients
#
#         for recipient in instance.recipients.all():
#             recipient.points_received += points_per_recipient
#             recipient.save()
#
#         instance.sender.points_available -= (total_points - remaining_points)
#         instance.sender.save()
#     else:
#         instance.sender.points_available -= total_points
#         instance.sender.save()
#
# # homepage/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Posts
#
# @receiver(post_save, sender=Posts)
# def update_sender_and_recipients_points(sender, instance, created, **kwargs):
#     if created:
#         total_points = instance.point
#         num_recipients = instance.recipients.all().count()
#
#         if num_recipients > 0:
#             points_per_recipient = total_points // num_recipients
#             remaining_points = total_points % num_recipients
#
#             for recipient in instance.recipients.all():
#                 recipient.points_received += points_per_recipient
#                 recipient.save()
#
#             instance.sender.points_available -= (total_points - remaining_points)
#             instance.sender.save()
#         else:
#             instance.sender.points_available -= total_points
#             instance.sender.save()


# @receiver(post_save, sender=Posts)
# def update_sender_and_recipients_points(sender, instance, created, **kwargs):
#     if created:
#         total_points = instance.point
#         num_recipients = instance.recipients.count()
#         print(f"total_points {total_points}, num_recipients {num_recipients}")
#
#         if num_recipients > 0:
#             points_per_recipient = total_points // num_recipients
#             remaining_points = total_points % num_recipients
#
#             for recipient in instance.recipients.all():
#                 recipient.points_received += points_per_recipient
#                 recipient.save()
#
#             instance.sender.points_available -= (total_points - remaining_points)
#             instance.sender.save()
#         else:
#             instance.sender.points_available -= total_points
#             instance.sender.save()

#
# @receiver(post_save, sender=Posts)
# def update_sender_and_recipients_points(sender, instance, created, **kwargs):
#     if created:
#         total_points = instance.point
#         num_recipients = instance.recipients.all().count()
#         # num_recipients = instance.recipients.count()
#         print(f"total_points {total_points}, num_recipients {num_recipients}")
#
#         if num_recipients > 0:
#             points_per_recipient = total_points // num_recipients
#             remaining_points = total_points % num_recipients
#
#             for recipient in instance.recipients.all():
#                 recipient.points_received += points_per_recipient
#                 recipient.save()
#
#             instance.sender.points_available -= total_points
#             instance.sender.save()
#         else:
#             instance.sender.points_available -= total_points
#             instance.sender.save()

#
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Posts
#
#
# @receiver(post_save, sender=Posts)
# def update_sender_and_recipients_points(sender, instance, created, **kwargs):
#     if created:
#         total_points = instance.point
#         num_recipients = instance.recipients.all().count()
#
#         if num_recipients > 0:
#             points_per_recipient = total_points // num_recipients
#             remaining_points = total_points % num_recipients
#
#             for recipient in instance.recipients.all():
#                 recipient.points_received += points_per_recipient
#                 recipient.save()
#
#                 if remaining_points > 0:
#                     recipient.points_received += 1
#                     recipient.save()
#                     remaining_points -= 1
#
#             instance.sender.points_available -= total_points
#             instance.sender.save()
#
# # homepage/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Posts
#
#
# @receiver(post_save, sender=Posts)
# def update_sender_and_recipients_points(sender, instance, created, **kwargs):
#     if created:
#         total_points = instance.point
#         num_recipients = instance.recipients.all().count()
#
#         if num_recipients > 0:
#             points_per_recipient = total_points // num_recipients
#             remaining_points = total_points % num_recipients
#
#             for recipient in instance.recipients.all():
#                 recipient.points_received += points_per_recipient
#                 recipient.save()
#
#             if remaining_points > 0:
#                 instance.recipients.first().points_received += remaining_points
#                 instance.recipients.first().save()
#
#         instance.sender.points_available -= total_points
#         instance.sender.save()

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

#
# @receiver(post_save, sender=Posts)
# def transfer_points(sender, instance, created, **kwargs):
#     if created:
#         sender = instance.sender
#         recipients = instance.recipients
#         point = instance.point
#         print(sender, " ", recipients," ",  point)
#
#         if sender.points_available < point:
#             return
#
#         with transaction.atomic():
#             if recipients.count() == 1:
#                 recipient = recipients.first()
#                 sender.points_available -= point
#                 recipient.points_received += point
#                 sender.save()
#                 recipient.save()
#             else:
#                 for recipient in recipients:
#                     recipient.points_received += point
#                     recipient.save()

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver


from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Posts)
def transfer_points(sender, instance, created, *args, **kwargs):
    if created:
        sender = instance.sender
        point = instance.point

        if sender.points_available < point:
            return

        recipients = instance.recipients.all()
        num_recipients = recipients.count()

        with transaction.atomic():
            if num_recipients == 1:
                recipient = recipients.first()
                sender.points_available -= point
                recipient.points_received += point
                sender.save()
                recipient.save()
            elif num_recipients > 1:
                for recipient in recipients:
                    recipient.points_received += point
                    recipient.save()

            # Always update the sender's points after handling recipients
            sender.points_available -= point
            sender.points_received += point
            sender.save()
