from django.db.models import F
from accounts.models import Account
from .models import Properties
from django_cron import CronJobBase, Schedule


class MonthlyUpdateCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'homepage.cron.monthly_update'

    def do(self):
        try:
            properties = Properties.objects.latest('id')
        except Properties.DoesNotExist:
            properties = Properties.objects.create()

        monthly_allowance = properties.monthly_allowance
        Account.objects.update(points_available=F('points_available') + monthly_allowance)
