FROM alpine:3.19

RUN apk add --no-cache \
    g++ \
    git \
    make \
    musl-dev \
    py3-pip \
    python3-dev

WORKDIR /opt/app

RUN git clone -q https://github.com/taku910/mecab.git /opt/mecab \
  && cd /opt/mecab/mecab \
  && ./configure --enable-utf8-only --with-charset=utf8 \
  && make > /dev/null \
  && make install \
  && rm -rf /opt/mecab/

RUN python3 -m venv /venv \
  && . /venv/bin/activate \
  && pip install gunicorn fugashi[unidic] \
  && python3 -m unidic download

WORKDIR /opt/app
COPY app.py /opt/app/
RUN adduser -D nonroot
USER nonroot

CMD ["/venv/bin/gunicorn", "-b", "0.0.0.0", "app"]
