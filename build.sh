# docker build -t wechatbot .
# docker run  --network host -it wechatbot:latest
# docker save -o wechatbot.tar wechatbot:latest

docker run -it -v $PWD/:/build/ python:3.6.15 bash

# pip install pypng PyQRCode requests pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple/ && pip install --upgrade revChatGPT -i https://pypi.tuna.tsinghua.edu.cn/simple/ && pip install itchat_uos-1.5.0.dev0-py3-none-any.whl
# pyinstaller -F -c --name wechatbot main.py
# pyinstaller -F -c --name wechatbot --collect-all main main.py
# pyinstaller -d all -F main.py
