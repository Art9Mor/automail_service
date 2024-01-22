from django.forms import ModelForm
from django.forms import DateTimeInput

from mailing.models import Mailing, Message, Client


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        user = self.request.user
        super().__init__(*args, **kwargs)
        self.fields['mail_to'].queryset = Client.objects.filter(owner=user)
        self.fields['message'].queryset = Message.objects.filter(owner=user)

    class Meta:
        model = Mailing
        exclude = ('next_date', 'owner', 'is_active',)

        widgets = {
            'start_date': DateTimeInput(attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ:СС', 'type': 'datetime-local'}),
            'end_date': DateTimeInput(attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ:СС', 'type': 'datetime-local'}),
        }


class MailingModeratorForm(StyleFormMixin, ModelForm):

    class Meta:
        model = Mailing
        fields = ('is_active',)


class MessageForm(StyleFormMixin, ModelForm):

    class Meta:
        model = Message
        exclude = ('owner',)


class ClientForm(StyleFormMixin, ModelForm):

    class Meta:
        model = Client
        exclude = ('owner',)