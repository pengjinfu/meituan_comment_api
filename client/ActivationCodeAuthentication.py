from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from active_code.models import ActiveCodeModel
from rest_framework.exceptions import AuthenticationFailed
import jwt
from jwt import ExpiredSignatureError


class ActivationCodeAuthentication(BaseAuthentication):
    def authenticate(self, request, *args, **kwargs):
        key: str = request.META.get('HTTP_KEY_AUTHORIZATION')

        if not key:
            raise AuthenticationFailed({'code': 441, 'msg': '请携带卡密'})

        ac = ActiveCodeModel.objects.filter(key=key).first()

        if ac is None:
            raise AuthenticationFailed({'code': 442, 'msg': '无效的卡密'})

        if ac.status == 0:
            raise AuthenticationFailed({'code': 443, 'msg': '卡密未激活'})
        if ac.status == 2:
            raise AuthenticationFailed({'code': 444, 'msg': '卡密已过期，请联系平台重新购买'})
        if ac.is_forbidden:
            raise AuthenticationFailed({'code': 445, 'msg': '您的卡密被滥用，已被禁止使用'})

        return ac, key
