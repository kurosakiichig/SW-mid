# 选择一个官方的轻量级Python镜像
FROM python:3.10-slim

# 设置容器中的工作目录
WORKDIR /app

# 把本地的所有代码复制到容器中
COPY . .

# 安装项目依赖
RUN pip install flask

# （如果你使用了 DeepSeek，需要安装 requests）
RUN pip install requests

# 暴露5000端口
EXPOSE 5000

# 启动Flask服务器
CMD ["python", "app.py"]
