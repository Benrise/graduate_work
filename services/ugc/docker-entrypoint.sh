#!/bin/bash

PORT=${UGC_SERVICE_PORT:-8003}

exec gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:${PORT} main:app