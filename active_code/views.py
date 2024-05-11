from rest_framework.views import APIView
from rest_framework.response import Response

import tools
from active_code.models import ActiveCodeModel
from active_code.serializers import ActiveCodeSerializer


class ActiveCodes(APIView):
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
