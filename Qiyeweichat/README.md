# Qiyeweichat
## 企业微信
下载之后解压到HA的配置目录，注意位置和权限：
```
root@S905W:/home/homeassistant/.homeassistant/custom_components/Qiyeweichat# ls -l
total 4
-rw-r----- 1 homeassistant homeassistant    0 Dec  2 17:42 __init__.py
-rw-r----- 1 homeassistant homeassistant 3959 Dec  2 17:42 notify.py
```
### 注册企业微信
1. 点击这里注册：https://work.weixin.qq.com/wework_admin/register_wx?from=myhome 1分钟时间注册下就行，比较简单。
2. 注册完成后打开：https://work.weixin.qq.com/wework_admin/frame#profile 复制下网页底部的企业信息中的企业ID备用。
Company ID	ww3ecf7f84de596c0c
3. 点击微工作台https://work.weixin.qq.com/wework_admin/frame#profile/wxPlugin
看到一个二维码,使用微信扫码关注,这样就可以使企业微信中收到的信息同步到微信上。

### 创建一个应用
1. 点击这里创建 https://work.weixin.qq.com/wework_admin/frame#apps/createApiApp
上传一个应用logo和自定义应用名字，其他默认。
AppName	fishy frog
2. 创建后打开：https://work.weixin.qq.com/wework_admin/frame#apps
可以看到在 "应用"中的"自建"里有个应用。点进去打开 记录下 AgentId和Secret备用。

修改配置文件configuration.yaml, 添加：
```
notify:
      - platform: Qiyeweichat
        name: fishyfrog
        corpid: 企业ID
        agentId: AgentId
        secret: Secret
        touser: '@all'
```
重启HomeAssistant，可以看到：

![screenshot](https://github.com/yaosheng79/HomeAssistant/blob/main/images/wecom.png?raw=true)
