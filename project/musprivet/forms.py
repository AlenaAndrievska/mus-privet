from django import forms
from .models import PaymentServiceByName, PaymentService, SongRequest, ServiceAdClipRequest, ServiceAdMusicRequest


class PaymentForm1(forms.ModelForm):
    class Meta:
        model = PaymentService
        fields = ['phone', 'email', 'congratulation']


class PaymentForm2(forms.ModelForm):
    class Meta:
        model = PaymentServiceByName
        fields = ['phone', 'email', 'service', 'congratulation']

class SongRequestForm(forms.ModelForm):
    class Meta:
        model = SongRequest
        fields = ['name', 'phone', 'email', 'message']

class ServiceAdClipRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceAdClipRequest
        fields = ['name', 'phone', 'email', 'timing', 'service', 'audio_file']


class ServiceAdMusicRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceAdMusicRequest
        fields = ['name', 'phone', 'email', 'service', 'audio_file']