FROM python:3.12-rc-slim-buster

WORKDIR /src

COPY src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ADD src/api_server.py .

CMD ["python","api_server.py"]

ENV APP_HOST="0.0.0.0"
ENV APP_PORT=8080
ENV REDIS_URL="redis"
ENV REDIS_PORT=6379

EXPOSE 8080