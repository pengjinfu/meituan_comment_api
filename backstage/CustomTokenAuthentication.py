from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from backstage.models import BackstageUserModel
from rest_framework.exceptions import AuthenticationFailed
import jwt
from jwt import ExpiredSignatureError


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request, *args, **kwargs):
        auth_token: str = request.META.get('HTTP_AUTHORIZATION')

        if not auth_token:
            raise AuthenticationFailed('请先登录')
        try:
            # token = auth_token.split(' ')[1] # 如果token形式如 JWT header.payload.signature 形式才需要这个操作
            payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = BackstageUserModel.objects.get(pk=user_id)
        except ExpiredSignatureError:
            raise AuthenticationFailed('登录已过期，请重新登录')
        except BackstageUserModel.DoesNotExist:
            raise BackstageUserModel.DoesNotExist('用户不存在')

        return user, auth_token
