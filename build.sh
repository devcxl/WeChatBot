#!/bin/bash
pyinstaller --clean wechatbot.spec
cp config.json ./dist/
docker build -t registry.cn-shanghai.aliyuncs.com/devcxl/wechatbot .
docker rm -f chatbot
docker run --network host --name chatbot -d registry.cn-shanghai.aliyuncs.com/devcxl/wechatbot:latest
docker system prune -f
docker push registry.cn-shanghai.aliyuncs.com/devcxl/wechatbot:latest