# -*- coding:utf-8 -*-


from django.template import RequestContext
from django.shortcuts import render_to_response
from apps.utils import server_define
from apps.game_manager.util import memcache
from apps.utils import model_define,game_define
from apps.common.decorators.decorators import require_permission
from apps.game_manager.mysql.server_list import get_server_list_dat
import hashlib
import pickle



# 获取玩家挑战BOSS信息
@require_permission
def get_boss_kyurem_info(request):
    head_lst = [
        {'width': 50, 'name': u'重置挑战次数'},
        {'width': 50, 'name': u'上次挑战时间'},
        {'width': 50, 'name': u'挑战BOSS次数'},
        {'width': 50, 'name': u'玩家鼓励值'},
        {'width': 50, 'name': u'是否领取奖励'}
        ]
    server_list_dat = get_server_list_dat()
    if request.method == 'POST':
        user_id = request.POST.get('user_uid')
        user_name = request.POST.get('user_name').encode('utf-8')
        user_account = request.POST.get('user_account')
        try:
            user_openid = str(request.POST.get('user_openid'))
        except UnicodeEncodeError :
            user_openid = ''

        server_id = int(request.POST.get('server_id'))
        type_hidden = 'visible'
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        state_list = game_define.USER_STATE_NAME_DICT
        row_lst=[]
        print user_id
        source=None
        print user_id
        source=None
        # f=open('/opt/CGameLogserver/apps/game_manager/views/data_edit/USER_DETAIL')
        # d=pickle.load(f)
        # for i in d:
        #     user_id=str(i)
        if cmem_url:
            if  len(user_id) <> 0:
                source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_WORLD_BOSS_KYUREM_MODEL.format(user_id=user_id))
                #print source,'source'
            elif  len(user_name)<> 0:
                name = hashlib.md5(user_name).hexdigest().upper()
                key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                source = memcache.get_cmem_val(cmem_url,model_define.PLAYER_WORLD_BOSS_KYUREM_MODEL.format(user_id=user_uid))
            elif  len(user_openid) <> 0:
                try:
                    result = memcache.get_cmem_val(cmem_url,model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_WORLD_BOSS_KYUREM_MODEL.format(user_id=result['uid']))
                except:
                    pass
            if source<> None :
                row_lst.append([str(source['reset_challenge_count']),str(source['last_play_datetime']),str(source['challenge_count']),str(source['player_inspire']),str(source['has_reward']),])
        return render_to_response("data_edit/boss_kyurem_info.html",
                                  {'row_lst': row_lst,'user_id':user_id,'user_openid':user_openid,'user_name':user_name,
                                   'head_lst': head_lst, 'server_list': server_list_dat,'cur_server_id':server_id}, RequestContext(request))
    else:
        row_lst = []
        return render_to_response("data_edit/boss_kyurem_info.html",
                                  {'row_lst': row_lst,
                                   'head_lst': head_lst, 'server_list': server_list_dat}, RequestContext(request))


def get_boss_snorlax_info(request):
    head_lst = [
        {'width': 50, 'name': u'重置挑战次数'},
        {'width': 50, 'name': u'上次挑战时间'},
        {'width': 50, 'name': u'挑战BOSS次数'},
        {'width': 50, 'name': u'玩家鼓励值'},
        {'width': 50, 'name': u'是否领取奖励'}
        ]
    server_list_dat = get_server_list_dat()
    if request.method == 'POST':
        user_id = request.POST.get('user_uid')
        user_name = request.POST.get('user_name').encode('utf-8')
        user_account = request.POST.get('user_account')
        try:
            user_openid = str(request.POST.get('user_openid'))
        except UnicodeEncodeError :
            user_openid = ''

        server_id = int(request.POST.get('server_id'))
        type_hidden = 'visible'
        cmem_url = server_define.CMEM_MAP[int(server_id)]
        state_list = game_define.USER_STATE_NAME_DICT
        row_lst=[]
        print user_id
        source=None
        if cmem_url:
            if  len(user_id) <> 0:
                source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_WORLD_BOSS_SNORLAX_MODEL.format(user_id=user_id))
                #print source,'source'
            elif  len(user_name)<> 0:
                name = hashlib.md5(user_name).hexdigest().upper()
                key = model_define.PLAYER_NICK_NAME_MODEL.format(player_nick_md5=name)
                user_uid = memcache.get_cmem_val_no_pick(cmem_url, key)
                source = memcache.get_cmem_val(cmem_url,model_define.PLAYER_WORLD_BOSS_SNORLAX_MODEL.format(user_id=user_uid))
            elif  len(user_openid) <> 0:
                try:
                    result = memcache.get_cmem_val(cmem_url,model_define.ACCOUNT_MAPPING_MODEL.format(open_id=user_openid))
                    source = memcache.get_cmem_val(cmem_url, model_define.PLAYER_WORLD_BOSS_SNORLAX_MODEL.format(user_id=result['uid']))
                except:
                    pass
            if source<> None :
                row_lst.append([str(source['reset_challenge_count']),str(source['last_play_datetime']),str(source['challenge_count']),str(source['player_inspire']),str(source['has_reward']),])
        return render_to_response("data_edit/boss_snorlax_info.html",
                                  {'row_lst': row_lst,'user_id':user_id,'user_openid':user_openid,'user_name':user_name,
                                   'head_lst': head_lst, 'server_list': server_list_dat,'cur_server_id':server_id}, RequestContext(request))
    else:
        row_lst = []
        return render_to_response("data_edit/boss_snorlax_info.html",
                                  {'row_lst': row_lst,
                                   'head_lst': head_lst, 'server_list': server_list_dat}, RequestContext(request))

