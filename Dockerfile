FROM alpine:latest

RUN apk add --no-cache \
    g++ \
    git \
    make \
    musl-dev \
    py3-pip \
    python3-dev

RUN mkdir /opt/app
COPY requirements.txt /tmp/

RUN git clone -q https://github.com/taku910/mecab.git /opt/mecab \
  && cd /opt/mecab/mecab \
  && ./configure --enable-utf8-only --with-charset=utf8 \
  && make > /dev/null \
  && make install \
  && pip3 install --no-cache-dir -q -r /tmp/requirements.txt \
  && python3 -m unidic download \
  && rm -rf /tmp/requirements.txt /opt/mecab/

WORKDIR /opt/app
COPY app.py /opt/app/
RUN adduser -D heroku
USER heroku

CMD ["gunicorn", "-b", "0.0.0.0", "app"]
