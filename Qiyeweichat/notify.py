"""
Qiyeweichat
{"message":"内容"}
{"message":"text|内容"}
{"message":"file|文件地址(<20MB)"}
{"message":"image|JPG,PNG文件地址(<2MB)"}
{"message":"voice|amr文件地址(<2MB, 60s)"}
{"title":"Homeassistant","message":"video|mp4本地地址(<10MB)"}
"""

import logging
import time
import datetime
import requests
import json,os
import voluptuous as vol
import sys

import logging
_LOGGER = logging.getLogger(__name__)

from homeassistant.components.notify import (
  ATTR_MESSAGE, ATTR_TITLE, ATTR_DATA, ATTR_TARGET, PLATFORM_SCHEMA, BaseNotificationService)
import homeassistant.helpers.config_validation as cv

CONF_CORPID = 'corpid'
CONF_AGENTID = 'agentId'
CONF_SECRET = 'secret'
CONF_TOUSER = 'touser'

def get_service(hass, config, discovery_info=None):
  corpid = config.get(CONF_CORPID)
  agentId = config.get(CONF_AGENTID)
  secret = config.get(CONF_SECRET)
  touser = config.get(CONF_TOUSER)
  return QiyeweichatNotificationService(hass, corpid, agentId, secret, touser)


class QiyeweichatNotificationService(BaseNotificationService):
  def __init__(self, hass, corpid, agentId, secret, touser):
    self.CORPID = corpid
    self.CORPSECRET = secret
    self.AGENTID = agentId
    self.TOUSER = touser

  def _get_access_token(self):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    values = {'corpid': self.CORPID,
              'corpsecret': self.CORPSECRET,
              }
    req = requests.post(url, params=values)
    data = json.loads(req.text)
    return data["access_token"]

  def get_access_token(self):
    access_token = self._get_access_token()
    return access_token

  def send_message(self, message='', **kwargs):
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
    title = kwargs.get(ATTR_TITLE)
    msgtype = message.split('|')[0]
    if msgtype == 'text':
      paylod = '"content":"' + message.split('|')[1] + '"'
    elif msgtype == 'image' or msgtype == 'video' or msgtype == 'voice' or msgtype == 'file':
      path = message.split('|')[1]
      curl = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=' + self.get_access_token() + '&type=' + msgtype
      files = {msgtype: open(path, 'rb')}
      r = requests.post(curl, files=files)
      re = json.loads(r.text)
      errcode = re['errcode']
      errmsg = re['errmsg']
      if errcode == 0:
        ree = re['media_id']
        media_id = str(ree)
        paylod = '"media_id":"' + media_id + '"'
        if title:
          paylod = paylod + ',"title":"' + title + '"'
      else:
        _LOGGER.error('error(' + errcode + '): ' + errmsg)
    else:
      msgtype = 'text'
      paylod = '"content":"' + message + '"'
    if paylod:
      send_data = '{"msgtype": "%s", "safe": "0", "agentid": %s, "touser": "%s", "%s": {%s}}' % (
          msgtype, self.AGENTID, self.TOUSER, msgtype, paylod)
      send_data8 = send_data.encode('utf-8')
      response = requests.post(send_url,send_data8)
