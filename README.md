保利威视云直播
--------------------


# Polyv's API
-------------


+ create_channel(password=None, player_color='#666666', auto_play=1)   **创建直播频道**

+ delete_channel(channel_id=None)  **删除直播频道**

+ get_channel(channel_id=None)  **查询直播频道信息**

+ get_channel_live(channel_id=None)  **查询直播频道是否在直播**

+ get_channel_realtime_watch_num(channel_id=None)  **获取实时观看人数**

+ set_max_viewer(channel_id=None, max_viewer=MAX_VIEWER)  **设置直播最大在线观看人数**

+ cutoff_channel(channel_id=None)  **禁播直播频道**

+ get_record_files(channel_id=None, start_date=None, end_date=None)  **获取直播录制文件**

+ get_channels_list()  **查询频道号列表**

+ update_channel_name(channel_id=None, name=None)  **修改频道名称**

+ update_channel_password(channel_id=None, password=None)  **修改频道密码**


# Usage
----------------

## Configure

在`polyv.conf.py`对以下参数进行配置。

APP_ID = 'egzkiq28qv'  # 保利威视提供的appID, 换成自己的。

APP_SECRET = '4a5e6b18237d4766a1f61a3771ad5734'  # 保利威视提供的app_secret，换成自己的。

USER_ID = 'edk3623tgk'  # 保利威视提供的用户ID， 换成自己的。

MAX_VIEWER = '100'  # 设置直播最大观看人数， 根据需求传入。



