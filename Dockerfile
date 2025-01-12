FROM python:3.12-alpine

WORKDIR /app

ARG USER_ID=1000
ARG GROUP_ID=1000

RUN addgroup -g $GROUP_ID -S apigroup && adduser -u $USER_ID -S apiuser -G apigroup /bin/sh

COPY --chown=apiuser . /app

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps gcc libc-dev make

USER apiuser

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]
