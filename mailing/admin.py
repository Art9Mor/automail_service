from django.contrib import admin

from mailing.models import Client, Message, Mailing, Logs


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'comment',)
    list_filter = ('name',)
    search_fields = ('name', 'email', 'comment')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'interval', 'status', 'owner')
    list_filter = ('start_date', 'end_date', 'interval', 'status', 'owner')
    search_fields = ('start_date', 'end_date')


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'last_mailing', 'status',)
