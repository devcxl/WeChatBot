#!/bin/bash
pyinstaller --clean wechatbot.spec
cp config.json ./dist/
docker build -t wechatbot .
docker rm -f chatbot
docker run --network host --name chatbot -d wechatbot:latest
docker system prune -f