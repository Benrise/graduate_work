FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y libatomic1 espeak ffmpeg

COPY . .
COPY ./docker-entrypoint.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8004

ENTRYPOINT ["docker-entrypoint.sh"]