from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from backstage.models import BackstageUserModel

import tools
from active_code.models import ActiveCodeModel
from active_code.serializers import ActiveCodeSerializer
from backstage.CustomTokenAuthentication import TokenAuthentication


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


class ActiveCodes(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        active_cdoes = ActiveCodeModel.objects.all()
        total = active_cdoes.count()
        serializer = ActiveCodeSerializer(active_cdoes, many=True)

        return Response(tools.api_response(200, 'ok', data=serializer.data, total=total))

    def post(self, request):
        life = request.data.get('life')

        if not str(life).isdigit():
            return Response(tools.api_response(401, '卡密有效期必须为有效的数字'))

        if life < 1:
            return Response(tools.api_response(401, '卡密有效期必须至少为1天'))

        key = tools.generate_unique_string()

        ac_q = ActiveCodeModel.objects.filter(key=key).first()

        if ac_q is not None:
            return Response(tools.api_response(500, '卡密生成重复，请稍后重试'))

        try:
            ac = ActiveCodeModel(
                key=key,
                life=life
            )

            ac.save()

            return Response(tools.api_response(200, '卡密生成成功'))
        except Exception as e:
            print(e)

        return Response(tools.api_response(501, '服务器异常,请稍后重试'))


class ActiveCodeDetail(APIView):
    authentication_classes = [TokenAuthentication]

    def put(self, request, ac_id, is_forbidden):
        try:
            is_forbidden = True if is_forbidden == 1 else False
            ac = ActiveCodeModel.objects.get(id=ac_id)
            ac.is_forbidden = not is_forbidden
            ac.save()
            return Response(tools.api_response(200, '操作成功'))
        except ActiveCodeModel.DoesNotExist:
            return Response(tools.api_response(400, '激活码不存在'))

        return Response(tools.api_response(500, '操作失败'))
