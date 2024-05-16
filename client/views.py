import datetime
import json
import traceback

from rest_framework.views import APIView
from rest_framework.response import Response

from mall.models import MallModel
from comment.models import CommentModel
from active_code.models import ActiveCodeModel
from mt_order.models import MTOrderModel
from mall.serializers import MallSerializer
from comment.serializers import CommentSerializer
from mt_order.serializer import MTOrderSerializer

from client.ActivationCodeAuthentication import ActivationCodeAuthentication

import tools

import spider.mall
import spider.comment


class Activation(APIView):
    def put(self, request):
        ac = request.data.get('active_code')

        try:
            ac_q = ActiveCodeModel.objects.get(key=ac, is_forbidden=False, status=0)
            activation_ip = ''

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
        except Exception as e:
            print(e)

        return Response(tools.api_response(401, '激活失败'))


class Malls(APIView):
    authentication_classes = [ActivationCodeAuthentication]

    def get(self, request):
        key = request.META.get('HTTP_KEY_AUTHORIZATION')
        ac = ActiveCodeModel.objects.get(key=key)
        malls = MallModel.objects.filter(active_code_id=ac.id)

        total = malls.count()

        serializer = MallSerializer(malls, many=True)

        malls_with_n_c = []
        for item in serializer.data:
            comments = CommentModel.objects.filter(poi_id=item['poi_id'])
            comments_count = comments.count()
            item.update({'n_comments_count': comments_count})
            malls_with_n_c.append(item)
        return Response(tools.api_response(200, 'ok', data=malls_with_n_c, total=total))

    def post(self, request):
        try:
            poi_id = request.data.get('poi_id')
            cookies = request.data.get('cookies')
            key = request.META.get('HTTP_KEY_AUTHORIZATION')
            active_code = ActiveCodeModel.objects.get(key=key)

            mall_info = spider.mall.get_mall_info(cookies)
            huifulv = spider.mall.get_mall_hui_fu_lv(cookies)

            if huifulv is None:
                return Response(tools.api_response(500, '回复率获取失败，请稍后再试'))

            if mall_info is None:
                return Response(tools.api_response(500, '门店信息获取失败,请稍后再试'))

            poi_name = mall_info['wmPoiName']

            mall = MallModel.objects.filter(poi_id=poi_id, active_code_id=active_code.id).first()

            if mall is not None:
                mall.cookies = cookies
                mall.poi_name = poi_name
                mall.huifulv = huifulv
                mall.save()
                return Response(tools.api_response(200, f'已更新门店{poi_name}的信息'))

            mall = MallModel(
                poi_id=poi_id,
                poi_name=poi_name,
                is_bind=True,
                status=1,
                cookies=cookies,
                active_code_id=active_code.id,
                huifulv=huifulv
            )
            mall.save()

            return Response(tools.api_response(200, '添加成功'))
        except Exception as e:
            print(e)
            return Response(tools.api_response(500, '添加失败'))


class MallDetail(APIView):
    authentication_classes = [ActivationCodeAuthentication]

    def get(self, request, mall_id):
        try:
            mall = MallModel.objects.get(pk=mall_id)
            serializer = MallSerializer(mall)

            return Response(tools.api_response(200, 'ok', data=serializer.data, total=1))
        except MallModel.DoesNotExist:
            return Response(tools.api_response(404, '店铺不存在'))


class Comments(APIView):
    authentication_classes = [ActivationCodeAuthentication]

    def get(self, requests, mall_id):
        try:
            mall = MallModel.objects.get(pk=mall_id)

            comments = CommentModel.objects.filter(poi_id=mall.poi_id)

            total = comments.count()

            serializer = CommentSerializer(comments, many=True)

            return Response(tools.api_response(200, '差评获取成功', data=serializer.data, total=total))

        except MallModel.DoesNotExist:
            return Response(tools.api_response(401, '无效的门店信息'))
        except Exception as e:
            traceback.print_exc()

        return Response(tools.api_response(500, '评论获取失败'))


class OrderDetail(APIView):
    authentication_classes = [ActivationCodeAuthentication]

    def get(self, request, comment_id):
        try:
            c = CommentModel.objects.get(pk=comment_id)
            food_details_src = json.loads(c.order_details)
            food_details_src = sorted(food_details_src, key=lambda item: item['foodName'])
            print(f'src: {food_details_src}')

            orders = MTOrderModel.objects.filter(poi_id=c.poi_id)

            ret_order = None
            for item in orders:
                food_details_dst = json.loads(item.food_details)
                food_details_dst = sorted(food_details_dst, key=lambda item: item['foodName'])
                if len(food_details_dst) == len(food_details_src):
                    print(f'dst: {food_details_dst}')
                    if tools.compare_food_list(food_details_src, food_details_dst):
                        order_serializer = MTOrderSerializer(item)
                        ret_order = order_serializer.data
                    # order_serializer = MTOrderSerializer(item)
                    # ret_order = order_serializer.data

            if ret_order is None:
                return Response(tools.api_response(404, msg='此评论对应的订单已过时效'))

            return Response(tools.api_response(200, '订单定位成功, 结果可能会有一定偏差，仅供参考', data=ret_order))
        except CommentModel.DoesNotExist:
            return Response(tools.api_response(404, '评价不存在'))
        except Exception as e:
            print(e)

        return Response(tools.api_response(500, '获取订单失败'))
