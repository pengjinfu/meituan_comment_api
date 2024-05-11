from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from backstage.models import BackstageUserModel
import tools


class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        captcha_code = request.data.get('captcha_code')

        # TODO: 验证图形验证码

        user = BackstageUserModel.objects.filter(username=username, password=tools.md5(password)).first()
        if not user:
            return Response(tools.api_response(404, '用户不存在或密码错误'))

        token = tools.generate_jwt(user.pk, user.username, settings.SECRET_KEY)

        return Response(tools.api_response(200, '登录成功', {'token': token}))
