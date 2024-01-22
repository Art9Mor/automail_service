from mailing.services import send_mailing
from mailing.models import MailingSettings


def daily_tasks():
    mailings = MailingSettings.objects.filter(period="Раз в день", status="Запущена")
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)


def weekly_tasks():
    mailings = MailingSettings.objects.filter(period="Раз в неделю", status="Запущена")
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)


def monthly_tasks():
    mailings = MailingSettings.objects.filter(period="Раз в месяц", status="Запущена")
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)