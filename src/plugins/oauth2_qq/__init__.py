# -*- coding: utf-8 -*-
"""
    passport.plugins.oauth2_qq
    ~~~~~~~~~~~~~~

    使用qq登录

    :copyright: (c) 2017 by staugur.
    :license: MIT, see LICENSE for more details.
"""

#: Importing these two modules is the first and must be done.
#: 首先导入这两个必须模块
from __future__ import absolute_import
from libs.base import PluginBase
#: Import the other modules here, and if it's your own module, use the relative Import. eg: from .lib import Lib
#: 在这里导入其他模块, 如果有自定义包目录, 使用相对导入, 如: from .lib import Lib
from flask import Blueprint, request, jsonify
from utils.web import OAuth2
from config import PLUGINS

#：Your plug-in name must be consistent with the plug-in directory name.
#：你的插件名称，必须和插件目录名称等保持一致.
__name__        = "oauth2_qq"
#: Plugin describes information. What does it do?
#: 插件描述信息,什么用处.
__description__ = "Connection QQ with OAuth2"
#: Plugin Author
#: 插件作者
__author__      = "Mr.tao <staugur@saintic.com>"
#: Plugin Version
#: 插件版本
__version__     = "0.1" 
#: Plugin Url
#: 插件主页
__url__         = "https://www.saintic.com"
#: Plugin License
#: 插件许可证
__license__     = "MIT"
#: Plugin License File
#: 插件许可证文件
__license_file__= "LICENSE"
#: Plugin Readme File
#: 插件自述文件
__readme_file__ = "README"
#: Plugin state, enabled or disabled, default: enabled
#: 插件状态, enabled、disabled, 默认enabled
__state__       = "disabled"

name = "qq"
qq = OAuth2(name,
    client_id = PLUGINS[name]["APP_ID"],
    client_secret = PLUGINS[name]["APP_KEY"],
    redirect_url = PLUGINS[name]["REDIRECT_URI"],
    authorize_url = "https://graph.qq.com/oauth2.0/authorize",
    access_token_url = "https://graph.qq.com/oauth2.0/token",
    get_userinfo_url = "https://graph.qq.com/oauth2.0/me"
)

plugin_blueprint = Blueprint("oauth2_qq", "oauth2_qq")
@plugin_blueprint.route("/login")
def login():
    """ 跳转此OAuth应用登录以授权
    此路由地址：/oauth2/qq/login
    """
    return qq.authorize()

@plugin_blueprint.route("/authorized")
def authorized():
    """ 授权回调路由
    此路由地址：/oauth2/qq/authorized
    """
    resp = qq.authorized_response()
    resp = qq.Parse_Access_Token(resp)
    print resp
    if resp and isinstance(resp, dict) and "access_token" in resp:
        user = github.get_userinfo(resp["access_token"])
        return jsonify(data=dict(
            resp=resp,
            user=user)
        )
    else:
        return 'Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description']
        )

#: 返回插件主类
def getPluginClass():
    return OAuth2_QQ_Main

#: 插件主类, 不强制要求名称与插件名一致, 保证getPluginClass准确返回此类
class OAuth2_QQ_Main(PluginBase):
    """ 继承自PluginBase基类 """

    def register_tep(self):
        """注册模板入口, 返回扩展点名称及扩展的代码, 其中include点必须是实际的HTML文件, string点必须是HTML代码."""
        tep = {"auth_signIn_socialLogin_string": """<a href="#" title="使用GitHub账号登录"><img src="/static/images/github.png" /></a>"""}
        return tep

    def register_bep(self):
        """注册蓝图入口, 返回蓝图路由前缀及蓝图名称"""
        bep = {"prefix": "/oauth2/github", "blueprint": plugin_blueprint}
        return bep