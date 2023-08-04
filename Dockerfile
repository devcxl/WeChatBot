FROM debian:12-slim
COPY ./dist/ /usr/bin/
CMD [ "wechatbot", "-f", "config.json" ]