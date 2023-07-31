FROM python:3.11.4-slim
WORKDIR /app
COPY . /app
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt && pip install itchat_uos-1.5.0.dev0-py3-none-any.whl
CMD [ "python3", "main.py", "--config", "config.json" ]