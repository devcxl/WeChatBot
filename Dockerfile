FROM debian:12-slim
WORKDIR /app
COPY ./dist/ /app/
CMD [ "./wechatbot", "-f", "config.json" ]