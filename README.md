# WeChatBot

WeChatBot是一款基于ItChat-UOS的微信聊天机器人，可以将你的微信小号快速接入OpenAI。

* 支持OpenAI的多个Api-Key轮询使用
* 支持OpenAI的Function call
* 支持OpenAI的Whisper语音识别
* 支持OpenAI的DALL-E-3画图

> 注意！！！
> - 使用该项目微信账号有被封禁的风险，请使用小号登陆。
> - 建议不要给太多人高频率使用，可能会导致账号被封禁。

## 部署

### Docker

```shell
docker run -d --name wechatbot \
-e TZ=Asia/Shanghai \
-e OPENAI_API_URL=https://your.proxy.domain.com/v1 \
-e OPENAI_API_KEYS=sk-xxxxxxxxxxxxxxxxxxxxxxxx,sk-xxxxxxxxxxxxxxxxxxxxxxxx \
devcxl/wechatbot:latest
```

### docker-compose

```yaml
version: '3.9'
services:
    wechatbot:
        image: devcxl/wechatbot:latest
        container_name: wechatbot
        environment:
            - TZ=Asia/Shanghai
            - OPENAI_API_URL=https://your.proxy.domain.com/v1
            - OPENAI_API_KEYS=sk-xxxxxxxxxxxxxxxxxxxxxxxx,sk-xxxxxxxxxxxxxxxxxxxxxxxx
        volumes:
            - ${PWD}/data/:/data
        restart: unless-stopped
```

### 登陆微信

查看`wechatbot`的日志

`docker logs wechatbot --tail 200 -f`

扫码登陆即可。

> 注意！！！
> - 无法登陆的情况建议给小号绑上银行卡再试。

## 环境变量

| 环境变量                     | 必需  | 默认值                          | 作用                                                 |
|--------------------------|-----|------------------------------|----------------------------------------------------|
| OPENAI_API_URL           | No  | https://api.openai.com/v1    | 设置OpenAI的接口                                        |
| OPENAI_API_KEYS          | Yes | None                         | 设置OpenAI的多个APIKey,使用`,`分割                          |
| MODEL                    | No  | gpt-3.5-turbo                | 设置对话使用的模型(建议使用带Function Call功能的模型)                 |
| DEFAULT_PROMPT           | No  | You are a helpful assistant. | 设置默认提示词                                            |
| HISTORY                  | No  | 15                           | 设置历史消息数                                            |
| DATA_DIR                 | No  | /data                        | 设置数据文件夹位置                                          |
| OPENAI_PROXY             | Yes | None                         | 设置请求OpenAI的HTTP/HTTPS代理(eg: http://127.0.0.1:8889) |
| PLUGIN_WEATHER_KEY       | No  | None                         | 高德地图的APIKey                                        |
| PLUGIN_EMAIL_SMTP_SERVER | No  | None                         | smtp服务器地址                                          |
| PLUGIN_EMAIL_SMTP_PORT   | No  | None                         | smtp服务器端口                                          |
| PLUGIN_EMAIL_ADDRESS     | No  | None                         | 邮箱发信地址                                             |
| PLUGIN_EMAIL_PASSWORD    | No  | None                         | 邮箱smtp密码                                           |

## 聊天指令

| 指令       | 功能           | 私聊  | 群聊 | 示例                                     |
|----------|--------------|-----|----|----------------------------------------|
| /clear   | 清理与GPT的聊天上下文 | Yes | No | `/clear`                               |
| /prompt  | 设置当前聊天的提示词   | Yes | No | `/prompt 请你充当一个专业的心理医生，请根据以下症状判断我的病症`  |
| /imagine | 使用DALL-E-3画图 | Yes | No | `/imagine 一只沙漠中的骆驼狂奔到了亚马逊雨林。真实风格，哈苏镜头` |

## FunctionCall插件

| 名称                  | 需要配置的环境变量                                                                                                 | 功能             | 使用示例                                      |
|---------------------|-----------------------------------------------------------------------------------------------------------|----------------|-------------------------------------------|
| get_current_weather | PLUGIN_WEATHER_KEY                                                                                        | 获取给定位置未来几天内的天气 | 明天上海天气怎么样，适合穿什么衣服                         |
| get_current_time    | None                                                                                                      | 获取当前时间         | 现在距离明天晚上八点还有多长时间                          |
| send_email          | PLUGIN_EMAIL_SMTP_SERVER,<br/>PLUGIN_EMAIL_SMTP_PORT,<br/>PLUGIN_EMAIL_ADDRESS,<br/>PLUGIN_EMAIL_PASSWORD | 向指定的邮箱发送邮件     | 给example@qq.com发封正式的商务邮件说我病了，明天的会议安排到下周一。 |

## 贡献FunctionCall插件

fork本项目，仿照在`function`包下`weather_function.py`创建自己想实现的功能开发即可

然后在`function`包下的`__init__.py`中仿照`WeatherFunction`进行注册

更新README.md中你开发的FunctionCall插件所需要的环境变量等信息

最后向本项目提交PR即可

## 相关项目

- https://github.com/littlecodersh/ItChat
- https://github.com/why2lyj/ItChat-UOS