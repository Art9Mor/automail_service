from datetime import datetime, timedelta
import pytz
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from mailing.models import Mailing, Logs


def my_job():
    day = timedelta(days=1, hours=0, minutes=0)
    weak = timedelta(days=7, hours=0, minutes=0)
    month = timedelta(days=30, hours=0, minutes=0)

    mailings = Mailing.objects.all().filter(status='Создана')\
        .filter(is_active=True)\
        .filter(next_date__lte=datetime.now(pytz.timezone('Asia/Novosibirsk')))\
        .filter(end_date__gte=datetime.now(pytz.timezone('Asia/Novosibirsk')))

    for mailing in mailings:
        mailing.status = 'Запущена'
        mailing.save()
        emails_list = [client.email for client in mailing.mail_to.all()]

        result = send_mail(
            subject=mailing.message.title,
            message=mailing.message.content,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails_list,
            fail_silently=False,
        )

        if result == 1:
            status = 'Отправлено'
        else:
            status = 'Ошибка отправки'

        log = Logs(mailing=mailing, status=status)
        log.save()

        if mailing.interval == 'ежедневно':
            mailing.next_date = log.last_mailing + day
        elif mailing.interval == 'раз в неделю':
            mailing.next_date = log.last_mailing + weak
        elif mailing.interval == 'раз в месяц':
            mailing.next_date = log.last_mailing + month
        elif mailing.interval == 'разовая':
            mailing.next_date = mailing.end_date

        if mailing.next_date < mailing.end_date:
            mailing.status = 'Создана'
        else:
            mailing.status = 'Завершена'
        mailing.save()


def get_cache_for_mailings():
    if settings.CACHE_ENABLED:
        key = 'mailings_count'
        mailings_count = cache.get(key)
        if mailings_count is None:
            mailings_count = Mailing.objects.all().count()
            cache.set(key, mailings_count)
    else:
        mailings_count = Mailing.objects.all().count()
    return mailings_count


def get_cache_for_active_mailings():
    if settings.CACHE_ENABLED:
        key = 'active_mailings_count'
        active_mailings_count = cache.get(key)
        if active_mailings_count is None:
            active_mailings_count = Mailing.objects.filter(is_active=True).count()
            cache.set(key, active_mailings_count)
    else:
        active_mailings_count = Mailing.objects.filter(is_active=True).count()
    return active_mailings_count
