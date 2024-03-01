FROM debian:12-slim
COPY ./dist/ /opt/
CMD [ "/opt/wechatbot", "-f", "/opt/config.prod.yaml" ]