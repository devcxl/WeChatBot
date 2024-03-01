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




```yaml
bot:
    chats:
        -   chat-1:
                type: friend


        -   chat-2:
                type: group

    friends:
        -   friend1:
                nick_name: xxxx
                remark_name: xxxx
        -   friend2:
                nick_name: xxxx
                remark_name: xxxx

    groups:
        -   group1:
                name:
                nick_name:
                remark_name:
                member:
                    -   member1:
                            nick_name: xxxx
                            remark_name: xxxx
                    -   member2:
                            nick_name: xxxx
                            remark_name: xxxx
``` 