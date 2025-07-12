FROM alpine:3.22.0

RUN apk add --no-cache socat

WORKDIR /

COPY battlebots .

CMD ["sh", "-c", "socat tcp-l:55555,fork,reuseaddr exec:./battlebots"]
