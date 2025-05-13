FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt;
COPY app ./app
COPY main.py .
COPY config.py .

COPY entrypoint.sh .
RUN chmod +x ./entrypoint.sh

ENV TZ=Asia/Shanghai
ENV PYTHONPATH="/app:$PYTHONPATH"
EXPOSE 7080/tcp
VOLUME /data
ENTRYPOINT ["/app/entrypoint.sh"]
