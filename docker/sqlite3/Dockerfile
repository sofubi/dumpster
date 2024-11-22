FROM alpine:latest

RUN apk --no-cache add sqlite

WORKDIR /db

COPY ./sqlite/init-db.sql /db/init/
RUN sqlite3 /data/test.db -init /db/init/init-db.sql

CMD ["sqlite3"]
