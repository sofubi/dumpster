FROM alpine:latest

RUN apk --no-cache add sqlite

WORKDIR /data
ADD ./test.db ./init-db.sql ./
RUN sqlite3 ./test.db < ./init-db.sql

CMD ["sqlite3"]
