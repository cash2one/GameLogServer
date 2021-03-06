# -*- coding:utf-8 -*-

import collections
import datetime
import time
import hashlib
from django.template import RequestContext
from apps.game_manager.views.log import daily_log
from django.shortcuts import render_to_response
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define
from apps.config import game_config
# 当前有用key
CUR_CON_STR_DIT = {
                    u"id": u' 完成的奖励任务',
                    u"stone": u' 奖励钻石： ', u"pokeBall": u' 奖励精灵球： ',
                    u"gold": u' 奖励金币： ',  u"experience": u' 奖励经验： ',
                    u"equipmentId": u' 奖励装备： ', u"times": u' 要求值：',
                    u'item2': u' 奖励物品2： ',
                    u'item1': u' 奖励物品1 ：', u'item3': u' 奖励物品3： ',
                  }
# 特殊处理的key
SPECIAL_CON_STR_LST = {u'item1': u'num1', u'item2': u'num2', u'item3': u'num3'}


# templates player_activity_treasure_ht.html
def get_player_activity_treasure_function(request, templates):
    """
        玩家运营数据编辑 夺宝
        source {'reward_end_date': datetime.date(2015, 8, 14),
                'single_activity_has_reward_lst': [1, 2],
                'version': u'20150715_5_35',
                'uid': '1000000950'

                'num': 35,
                }
        config_dict   {"stone": 50, "pokeBall": 1, "num1": 0, "gold": 0, "num3": 0, "item2": 0, "item3": 0, "item1": 0,
                        "equipmentId": 0, "experience": 100, "times": 10, "num2": 0, "id": 1},
    """
    # 以函数的指针方式传递函数并调用
    function_name = 'data_edit.player_activity_treasure_py.{function}'.format(function=set_player_activity_treasure_function.__name__)
    print 'function_name', function_name
    server_list, platform_list = daily_log._get_server_list(None, None)
    try:
        server_list.remove(server_list[0])
    except:
        pass

    return_uid = '请输入uid'
    return_openid = "请输入openid"
    return_name = "请输入玩家昵称"
    if request.method == 'POST':
        user_uid = request.POST.get('user_uid')
        user_name = request.POST.get('user_name').encode('utf-8')
        user_openid = request.POST.get('user_openid')
        server_id = int(request.POST.get('server_id'))
        type_hidden = 'visible'
        cmem_url = server_define.CMEM_MAP[int(server_id)]

        head_lst = [
            {'name': u'名称'},
            {'name': u'数量'},
        ]
        if cmem_url:
            try:
                source = dict()
                if len(user_uid):
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_ACTIVITY_TREASURE_MODEL.format(user_id=user_uid))
                elif len(user_name):
                    name = hashlib.md5(user_name).hexdigest().upper()
                    key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                    user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                    return_name = user_name
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_ACTIVITY_TREASURE_MODEL.format(user_id=user_uid))
                elif len(user_openid):
                    result = memcache.get_cmem_val(cmem_url, model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    user_uid = result['uid']
                    return_openid = user_openid
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_ACTIVITY_TREASURE_MODEL.format(user_id=user_uid))
                if source:
                    # print 'source', source
                    row_dict = collections.OrderedDict()  # 有序字典
                    # -----------------------------------不可改元素---------------------------------------------------------------#
                    # [[[0,1],[0,1]],[[0,1],[0,1]]] 三层[]
                    # ------------------------用户UID
                    uid = source.get('uid', 'None')
                    if uid != 'None':
                        uid_lst = [[u'用户UID', uid]]
                    else:
                        uid_lst = []
                    # ------------------运营活动奖励结束时间
                    try:
                        reward_end_date = source['reward_end_date'].strftime('%Y-%m-%d')   # 运营活动奖励结束时间
                        reward_end_date_lst = [[u'运营活动奖励结束时间', reward_end_date]]
                    except:
                        reward_end_date_lst = []
                    # ------------------运营活动当前版本
                    try:
                        version = source['version']   # 运营活动当前版本
                        version_lst = [[u'运营活动当前版本', version]]
                    except:
                        version_lst = []
                    # ---------------- 玩家奖励信息
                    try:
                        reward_lst = source.get('single_activity_has_reward_lst', [])                   # [1,2,3,4,5]
                        reward_str = ''                                                                 # 字符串
                        cur_reward_config_lst = game_config.get_all_reward_times_treasure_config()  # 策划填的配置表
                        if reward_lst:
                            for reward_id in reward_lst:
                                each_conf_lst = cur_reward_config_lst[str(reward_id)]       # 取出每条配置表
                                for key, each_int_value in each_conf_lst.items():           # 遍历每个key 值
                                    if each_int_value:                                      # 有值
                                        if key in CUR_CON_STR_DIT:                          # 且在配置字典
                                            if key in SPECIAL_CON_STR_LST.keys():           # 是特殊处理key
                                                each_item_str = game_config.get_item_config(each_int_value)['name']  # 取物品名
                                                each_item_str += u"： "
                                                each_item_val = each_conf_lst[SPECIAL_CON_STR_LST[key]]              # 取数量
                                            else:
                                                each_item_str = CUR_CON_STR_DIT[key]                         # 取物品名
                                                each_item_val = each_int_value                               # 取数量
                                            reward_str += each_item_str                                      # 字符串拼接名字
                                            reward_str += str(each_item_val) + ";   "                        # 字符串拼接值
                                        else:
                                            continue
                                    else:
                                        continue
                                reward_str += '-----------'
                            reward_lst = [[u'玩家奖励信息',reward_str]]
                            # print reward_lst
                    except:
                        reward_lst = []
                    # ------------------- 汇总 有就加入总表（三层列表 [[[],[]],[[],[]]]）
                    all_immutable_lst = []
                    if uid_lst:
                        all_immutable_lst.append(uid_lst)
                    if reward_end_date_lst:
                        all_immutable_lst.append(reward_end_date_lst)
                    if version_lst:
                        all_immutable_lst.append(version_lst)
                    if reward_lst:
                        all_immutable_lst.append(reward_lst)
                    # -------------------------------------------------------------------------------------------------------------------#
                    # -----------------------------------可改元素-------------------------------------------------------------------------#
                    # {key1:{'name':X,'num':X},key2:{'name':X,'num':X}}
                    # 夺宝到达次数
                    treasure_win_count = source.get('num', 'None')
                    if treasure_win_count != 'None':
                        row_dict['treasure_win_count'] = {'name': u'夺宝到达次数', 'num': treasure_win_count}
                    # -----------------------------------------------------------------------------------------------------------------------#
                else:
                    if user_uid:
                        return_uid = user_uid
                        if user_openid:
                            return_openid = user_openid
                        if user_name:
                            return_name = user_name

                return render_to_response(templates, locals(), RequestContext(request))

            except UnboundLocalError:
                type_hidden = 'hidden'
                return render_to_response(templates, locals(), RequestContext(request))

            except TypeError:
                type_hidden = 'hidden'
                return render_to_response(templates, locals(), RequestContext(request))

    else:
        row_list = []
        type_hidden = 'hidden'
        return render_to_response(templates, locals(), RequestContext(request))


# @require_permission
def set_player_activity_treasure_function(value_dict):
    """
    修改memcache数据

    value_dict['tem_id'] treasure_win_count
    value_dict['input_value'] int
    """
    cmem_url = server_define.CMEM_MAP[int(value_dict['server_id'])]
    if cmem_url:
        if len(value_dict['user_id']):
            source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_ACTIVITY_TREASURE_MODEL.format(user_id=value_dict['user_id']))
            try:
                key = value_dict['item_id']
                if int(value_dict['input_value']) >= 0 and 'treasure_win_count' == key:
                    source['num'] = int(value_dict['input_value'])
                else:
                    return False
            except:
                return False
            # 传回 url  uid  以及数据 做外层检测
            result = memcache.put_cmem_val(cmem_url, model_define.PLAYER_ACTIVITY_TREASURE_MODEL.format(user_id=value_dict['user_id']), source)
            return result