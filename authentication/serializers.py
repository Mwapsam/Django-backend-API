from rest_framework import serializers
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from .models import User
from .token import account_activation_token

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = User
        fields = ['id', 'firstname', 'lastname', 'email', 'phoneNumber', 'password']

    def create(self, validate_data):
        regUser = User.objects.create(**validate_data)
        regUser.set_password(validate_data['password'])
        regUser.save()
        mail_subject = 'Profiles: Registration'
        message = render_to_string('reg_conf_mail.html', {
            'user_display': regUser.firstname,
            'site': settings.FRONTEND_URL,
            'uid': urlsafe_base64_encode(force_bytes(regUser.pk)),
            'token': account_activation_token.make_token(regUser),
            'email': regUser.email
        })
        send_mail(mail_subject,
                  message,
                  settings.DEFAULT_FROM_EMAIL,
                  [regUser.email], fail_silently=False)

        if regUser:
            return regUser
        return Response({
            'error': 'Something went wrong'
        }, status=400)