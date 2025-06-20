FROM alpine:3.22.0

RUN apk add --no-cache socat

WORKDIR /

COPY flagbin .

CMD ["sh", "-c", "mkdir -p /tmp/flags && socat tcp-l:52420,fork,reuseaddr exec:./flagbin"]

