FROM python:3.11.4-slim
WORKDIR /app
COPY . /app
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt && pip install git+https://github.com/devcxl/wechat-api.git
CMD [ "python3", "main.py", "--config", "config.json" ]