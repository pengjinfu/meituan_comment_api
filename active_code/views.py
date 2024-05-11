import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

import tools
from active_code.models import ActiveCodeModel
from active_code.serializers import ActiveCodeSerializer
from backstage.CustomTokenAuthentication import TokenAuthentication


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


class Activation(APIView):
    def put(self, request):
        ac = request.data.get('active_code')

        try:
            ac_q = ActiveCodeModel.objects.get(key=ac, is_forbidden=False, status=0)
            activation_ip = ''

            # if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                activation_ip = request.META['HTTP_X_FORWARD_FOR']
            else:
                activation_ip = request.META['REMOTE_ADDR']
            aid = ac_q.pk
            status = 1
            life = ac_q.life
            active_time = datetime.datetime.now()
            expire = active_time + datetime.timedelta(days=life)

            ac_q.status = status
            ac_q.active_time = active_time
            ac_q.expire = expire
            ac_q.activation_ip = activation_ip
            ac_q.save()

            return Response(tools.api_response(200, '激活成功', {'aid': aid}))
        except ActiveCodeModel.DoesNotExist:
            print('激活码不存在')
            return Response(tools.api_response(401, '卡密无效'))
