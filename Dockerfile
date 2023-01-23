FROM python:3.10.9-alpine3.17 as builder
RUN apk --no-cache add gcc musl-dev linux-headers python3-dev libev-dev
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.10.9-alpine3.17
RUN apk --no-cache update && apk --no-cache add libev-dev \
    && adduser -D app
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
WORKDIR /app
COPY --chown=app:app . .
USER app
ENTRYPOINT ["python3"]
CMD ["server.py"]
