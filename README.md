# 微信聊天机器人

## docker部署

```shell
docker run -d --name wechatbot \
-e TZ=Asia/Shanghai \
-e OPENAI_API_URL=https://your.proxy.domain.com/v1 \
-e OPENAI_API_KEYS=sk-xxxxxxxxxxxxxxxxxxxxxxxx,sk-xxxxxxxxxxxxxxxxxxxxxxxx \
ghcr.io/devcxl/wechatbot:latest
```

## docker-compose部署

```yaml
version: '3.9'
services:
    wechatbot:
        image: ghcr.io/devcxl/wechatbot:latest
        container_name: wechatbot
        environment:
            - TZ=Asia/Shanghai
            - OPENAI_API_URL=https://your.proxy.domain.com/v1
            - OPENAI_API_KEYS=sk-xxxxxxxxxxxxxxxxxxxxxxxx,sk-xxxxxxxxxxxxxxxxxxxxxxxx
        volumes:
            - ${PWD}/data/:/data
        restart: unless-stopped
```

### 登陆

`docker logs wechatbot --tail 200 -f`

扫描控制台的二维码登陆

## 环境变量

| KEY             | DEFAULT                      | detail                |
|-----------------|------------------------------|-----------------------|
| OPENAI_API_URL  | https://api.openai.com/v1    | OPENAI的接口             |
| OPENAI_API_KEYS | None                         | OPENAI的ApiKey,使用`,`分割 |
| MODEL           | gpt-3.5-turbo                | 对话使用的模型               |
| DEFAULT_PROMPT  | You are a helpful assistant. | 默认提示词                 |
| HISTORY         | 15                           | 历史消息数                 |
| DATA_DIR        | /data                        | 数据文件夹                 |
| OPENAI_PROXY    | None                         | 请求OPENAI的代理           |


