# -*- coding: utf-8 -*-
"""
    passport.libs.base
    ~~~~~~~~~~~~~~

    Base class: dependent services, connection information, and public information.

    :copyright: (c) 2017 by staugur.
    :license: MIT, see LICENSE for more details.
"""

import json
from utils.tool import logger, plugin_logger, create_redis_engine, create_mysql_engine


class ServiceBase(object):
    """ 所有服务的基类 """

    def __init__(self):
        #设置全局超时时间(如连接超时)
        self.timeout = 2
        self.redis = create_redis_engine()
        self.mysql = create_mysql_engine()

    @property
    def listAdminUsers(self):
        """ 用户列表缓存 """
        key = "passport:user:admins"
        try:
            data = json.loads(self.redis.get(key))
            logger.info("Hit listAdminUsers Cache")
        except:
            sql = "SELECT uid FROM user_profile WHERE is_admin = 1"
            data = [ item['uid'] for item in self.mysql.query(sql) ]
            pipe = self.redis.pipeline()
            pipe.set(key, json.dumps(data))
            pipe.expire(key, 600)
            pipe.execute()
        return data

    @property
    def refreshAdminUsers(self):
        """ 刷新管理员列表缓存 """
        key = "passport:user:admins"
        return True if isinstance(self.redis.delete(key), (int, long)) else False

    def isAdmin(self, uid):
        """ 判断是否为管理员 """
        return uid in self.listAdminUsers


class PluginBase(ServiceBase):
    """ 插件基类: 提供插件所需要的公共接口与扩展点 """
    
    def __init__(self):
        super(PluginBase, self).__init__()
        self.logger = plugin_logger
