# 微信聊天机器人

## 构建

`bash build.sh`

## 部署

```shell
#!/bin/bash
cd workdir
docker rm -f wechatbot
docker pull registry.cn-shanghai.aliyuncs.com/devcxl/wechatbot:latest
docker-compose up -d wechatbot
docker ps -a | grep wechatbot
docker logs --tail 1000 -f wechatbot
```