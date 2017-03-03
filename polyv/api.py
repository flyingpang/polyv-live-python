# coding: utf-8
__author__ = 'flyingpang'
"""Create at 2017.02.27"""
import time
import uuid
import datetime
import requests
from polyv.conf import APP_ID, APP_SECRET, USER_ID, MAX_VIEWER
from polyv.exceptions import RequestException, MissingParameterException
from polyv.utils import make_sign


# 创建直播频道
def create_channel(password=None, player_color='#666666', auto_play=1):
    """
    :param password: 直播频道密码
    :param player_color: 播放器控制栏颜色, 默认#666666
    :param auto_play: 是否自动播放,0/1,默认1
    :return: 成功或失败的json信息
    """
    url = 'http://api.live.polyv.net/web/v1/channels/'
    app_id = APP_ID
    app_secret = APP_SECRET
    timestamp = int(time.time())
    name = 'channel_name' + str(uuid.uuid4())[:8]
    if not password:
        password = str(uuid.uuid4())[:6]
    user_id = USER_ID
    str1 = "{app_secret}appId{app_id}autoPlay{autoplay}channelPasswd{password}name{name}playerColor{player_color}timestamp{timestamp}userId{user_id}{app_secret}".format(app_secret=app_secret, app_id=app_id, autoplay=auto_play, password=password, name=name, player_color=player_color, timestamp=timestamp, user_id=user_id)

    params = dict()
    params.update({
        'appId': app_id,
        'autoPlay': auto_play,
        'name': name,
        'playerColor': player_color,
        'timestamp': timestamp,
        'userId': user_id,
        'channelPasswd': password,
        'sign': make_sign(str1)
    })
    response = requests.post(url, params=params)

    if response.json()['status'] != 'success':
        raise RequestException(response.text)

    return response.json()['result']


# 删除直播频道
def delete_channel(channel_id=None):
    """
    :param channel_id: 在线直播系统登陆的频道ID.
    :return: 删除成功返回True, 否则返回False.
    """
    if not channel_id:
        raise MissingParameterException("missing channel_id parameter.")

    url = 'http://api.live.polyv.net/v1/channels/{channel_id}'.format(channel_id=channel_id)
    app_id = APP_ID
    app_secret = APP_SECRET
    timestamp = int(time.time())
    user_id = USER_ID
    str1 = '{app_secret}appId{app_id}timestamp{timestamp}userId{user_id}{app_secret}'.format(app_secret=app_secret, app_id=app_id, timestamp=timestamp, user_id=user_id)

    params = dict()
    params.update({
        'appId': app_id,
        'timestamp': timestamp,
        'userId': user_id,
        'sign': make_sign(str1)
    })
    response = requests.delete(url, params=params)

    if response.json()['status'] != 'success':
        raise RequestException(response.text)

    return response.status_code == 200


# 查询直播频道信息
def get_channel(channel_id=None):
    """
    :param channel_id: 在线直播系统登陆的频道ID.
    :return: channel_id的直播频道信息.
    """
    if not channel_id:
        raise MissingParameterException("missing channel_id parameter.")

    url = 'http://api.live.polyv.net/v1/channels/{channel_id}'.format
    app_id = APP_ID
    app_secret = APP_SECRET
    timestamp = int(time.time())
    user_id = USER_ID

    str1 = "{app_secret}appId{app_id}timestamp{timestamp}userId{user_id}{app_secret}".format(app_secret=app_secret, app_id=APP_ID, timestamp=timestamp, user_id=user_id)
    url = 'http://api.live.polyv.net/v1/channels/{channel_id}?appId={app_id}&timestamp={timestamp}&userId={user_id}&sign={sign}'.format(channel_id=channel_id, app_id=app_id, timestamp=timestamp, user_id=user_id, sign=make_sign(str1))
    response = requests.get(url)

    if response.json()['status'] != 'success':
        raise RequestException(response.text)

    return response.json()['result']


# 查询直播频道是否在直播
def get_channel_live(channel_id=None):
    """
    :param channel_id: 在线直播系统登陆的频道ID.
    :return: 如果正在直播状态返回True,否则返回False.
    """
    if not channel_id:
        raise MissingParameterException("missing channel_id parameter.")

    url = "http://api.live.polyv.net/live_status/query"
    stream = get_channel(channel_id).get('stream')
    response = requests.get(url, data={'stream': stream})

    if response.status_code != 200:
        raise RequestException(response.text)

    return response == 'live'


# 获取实时观看人数
def get_channel_realtime_watch_num(channel_id=None):
    """
    :param channel_id: 在线直播系统登陆的频道ID.
    :return: 15组每8秒统计的观看人数.
    """
    if not channel_id:
        raise MissingParameterException("missing channel_id parameter.")

    app_id = APP_ID
    app_secret = APP_SECRET
    timestamp = int(time.time())
    user_id = USER_ID
    str1 = "{app_secret}appId{app_id}timestamp{timestamp}userId{user_id}{app_secret}".format(app_secret=app_secret, app_id=APP_ID, timestamp=timestamp, user_id=user_id)

    url = "http://api.live.polyv.net/v1/statistics/{channel_id}/realtime?appId={app_id}&timestamp={timestamp}&userId={user_id}&sign={sign}".format(channel_id=channel_id, app_id=app_id, timestamp=timestamp, user_id=user_id, sign=make_sign(str1))
    response = requests.get(url)

    if response.json()['status'] != 'success':
        raise RequestException(response.text)

    return response.json()['result']


# 设置直播最大在线观看人数
def set_max_viewer(channel_id=None, max_viewer=MAX_VIEWER):
    """
    :param channel_id: 在线直播系统登陆的频道ID.
    :param max_viewer: 设置直播最大观看人数.
    :return:
    """
    if not channel_id:
        raise MissingParameterException("missing channel_id parameter.")
    if not max_viewer:
        raise MissingParameterException("missing max_viewer parameter.")

    app_id = APP_ID
    app_secret = APP_SECRET
    timestamp = int(time.time())
    user_id = USER_ID
    str1 = "{app_secret}appId{app_id}maxViewer{max_viewer}timestamp{timestamp}userId{user_id}{app_secret}".format(app_secret=app_secret, app_id=app_id, max_viewer=max_viewer, timestamp=timestamp, user_id=user_id)

    url = 'http://api.live.polyv.net/v1/restrict/{channel_id}/update?appId={app_id}&timestamp={timestamp}&userId={user_id}&maxViewer={max_viewer}&sign={sign}'.format(channel_id=channel_id, app_id=app_id, timestamp=timestamp, user_id=user_id, max_viewer=max_viewer, sign=make_sign(str1))
    response = requests.post(url)

    if response.json()['status'] != 'success':
        raise RequestException(response.text)

    return response.json()['status'] == 'success'


# 禁播直播频道
def cutoff_channel(channel_id=None):
    """
    :param channel_id: 在线直播系统登陆的频道ID.
    :return: 截断成功返回True, 否则返回False.
    """
    if not channel_id:
        raise MissingParameterException("missing channel_id parameter.")

    url = "http://api.live.polyv.net/v1/stream/{channel_id}/cutoff".format(channel_id=channel_id)
    app_id = APP_ID
    app_secret = APP_SECRET
    timestamp = int(time.time())
    user_id = USER_ID

    str1 = "{app_secret}appId{app_id}timestamp{timestamp}userId{user_id}{app_secret}".format(app_secret=app_secret, app_id=app_id, timestamp=timestamp, user_id=user_id)
    data = dict()
    data.update({
        'appId': app_id,
        'timestamp': timestamp,
        'userId': user_id,
        'sign': make_sign(str1)
    })
    response = requests.post(url, data=data)

    return response.json()['status'] == 'success'


# 获取直播录制文件
def get_record_files(channel_id=None, start_date=None, end_date=None):
    """
    :param channel_id: 在线直播系统登陆的频道ID.
    :param start_date: 查询起始时间.
    :param end_date: 查询终止时间.
    :return:
    """
    if not channel_id:
        raise MissingParameterException("missing channel_id parameter.")

    app_id = APP_ID
    app_secret = APP_SECRET
    timestamp = int(time.time())
    user_id = USER_ID
    if not start_date:
        start_date = datetime.datetime.today().strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.datetime.today().strftime('%Y-%m-%d')
    str1 = "{app_secret}appId{app_id}endDate{end_date}startDate{start_date}timestamp{timestamp}userId{user_id}{app_secret}".format(app_secret=app_secret, app_id=app_id, start_date=start_date, end_date=end_date, timestamp=timestamp, user_id=user_id)

    url = "http://api.live.polyv.net/v1/channels/{channel_id}/recordFiles?appId={app_id}&endDate={end_date}&startDate={start_date}&timestamp={timestamp}&userId={user_id}&sign={sign}".format(channel_id=channel_id, app_id=app_id, start_date=start_date, end_date=end_date, timestamp=timestamp, user_id=user_id, sign=make_sign(str1))
    response = requests.get(url)

    if response.json()['status'] != 'success':
        raise RequestException(response.text)

    return response.json()['result']


# 查询频道号列表
def get_channels_list():
    """
    :return: list形式的频道号.
    """
    app_id = APP_ID
    app_secret = APP_SECRET
    timestamp = int(time.time())
    user_id = USER_ID
    str1 = "{app_secret}appId{app_id}timestamp{timestamp}{app_secret}".format(app_secret=app_secret, app_id=app_id, timestamp=timestamp)

    url = "http://api.live.polyv.net/v1/users/{user_id}/channels?appId={app_id}&timestamp={timestamp}&sign={sign}".format(user_id=user_id, app_id=app_id, timestamp=timestamp, sign=make_sign(str1))
    response = requests.get(url)

    if response.json()['status'] != 'success':
        raise RequestException(response.text)

    return response.json()['result']


# 修改频道名称
def update_channel_name(channel_id=None, name=None):
    """
    :param channel_id: 在线直播系统登陆的频道ID.
    :param name: 要修改的频道名称
    :return: 成功返回True, 否则返回False
    """
    if not channel_id:
        raise MissingParameterException("missing channel_id parameter.")
    if not name:
        raise MissingParameterException("missing name parameter.")

    app_id = APP_ID
    app_secret = APP_SECRET
    timestamp = int(round(time.time() * 1000))
    str1 = "{app_secret}appId{app_id}name{name}timestamp{timestamp}{app_secret}".format(app_secret=app_secret, app_id=app_id, name=name, timestamp=timestamp)

    url = "http://api.live.polyv.net/v2/channels/{channel_id}/update?appId={app_id}&timestamp={timestamp}&name={name}&sign={sign}".format(channel_id=channel_id, app_id=app_id, timestamp=timestamp, name=name, sign=make_sign(str1))
    response = requests.post(url)

    return response.json()['status'] == 'success'


# 修改频道密码
def update_channel_password(channel_id=None, password=None):
    """
    :param channel_id: 在线直播系统登陆的频道ID.
    :param password: 需要修改的密码.
    :return: 如果修改成功返回True, 否则返回False.
    """
    if not channel_id:
        raise MissingParameterException("missing channel_id parameter.")
    if not password:
        raise MissingParameterException("missing password parameter.")

    app_id = APP_ID
    app_secret = APP_SECRET
    timestamp = int(round(time.time() * 1000))
    user_id = USER_ID
    str1 = "{app_secret}appId{app_id}channelId{channel_id}passwd{password}timestamp{timestamp}{app_secret}".format(app_secret=app_secret, app_id=app_id, password=password, channel_id=channel_id, timestamp=timestamp)

    url = "http://api.live.polyv.net/v2/channels/{user_id}/passwdSetting?appId={app_id}&timestamp={timestamp}&channelId={channel_id}&passwd={password}&sign={sign}".format(user_id=user_id, app_id=app_id, timestamp=timestamp, channel_id=channel_id, password=password, sign=make_sign(str1))
    response = requests.post(url)

    return response.json()['status'] == "success"
