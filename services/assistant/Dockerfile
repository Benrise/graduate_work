FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    espeak \
    ffmpeg \
    libatomic1 \
    build-essential

COPY requirements.txt .

RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

COPY . .
COPY ./docker-entrypoint.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8004

ENTRYPOINT ["docker-entrypoint.sh"]