from rest_framework.serializers import Serializer, CharField, EmailField, ValidationError
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class CustomAuthTokenSerializer(Serializer):
    email = EmailField(
        label=_("Email"),
        write_only=True
    )
    password = CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                raise AuthenticationFailed()
        else:
            msg = _('Must include "email" and "password".')
            raise ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
