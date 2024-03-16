#!/bin/bash
pyinstaller --clean wechatbot.spec
docker build -t registry.cn-shanghai.aliyuncs.com/devcxl/wechatbot:dev .
docker system prune -f
docker push registry.cn-shanghai.aliyuncs.com/devcxl/wechatbot:dev