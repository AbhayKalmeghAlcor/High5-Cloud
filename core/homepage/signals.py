from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Posts


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


@receiver(pre_save, sender=Posts)
def update_sender_and_recipients_points(sender, instance, **kwargs):
    total_points = instance.point
    num_recipients = instance.recipients.count()
    print(f"total_points {total_points}, num_recipients {num_recipients}")

    if num_recipients > 0:
        points_per_recipient = total_points // num_recipients
        remaining_points = total_points % num_recipients

        for recipient in instance.recipients.all():
            recipient.points_received += points_per_recipient
            recipient.save()

        instance.sender.points_available -= (total_points - remaining_points)
        instance.sender.save()
    else:
        instance.sender.points_available -= total_points
        instance.sender.save()
