#!/bin/bash

PORT=${API_SERVICE_PORT:-8000}

exec gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:${PORT} main:app