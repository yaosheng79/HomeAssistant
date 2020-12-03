# hello_miai
## 小爱同学TTS
复制到HA的配置目录，注意位置和权限：
```
root@S905W:/home/homeassistant/.homeassistant/custom_components/hello_miai# ls -l
-rw-r----- 1 homeassistant homeassistant 19508 Dec  2 11:10 __init__.py
-rw-r----- 1 homeassistant homeassistant   176 Dec  2 11:10 manifest.json
-rw-r----- 1 homeassistant homeassistant  1393 Dec  2 11:10 services.yaml
```
修改配置文件configuration.yaml, 添加：
```
hello_miai:
        miid: '1863991862'
        password: 'Abc12345'
```
重启HomeAssistant，可以看到：

