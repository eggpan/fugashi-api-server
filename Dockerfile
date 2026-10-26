FROM alpine:3.24

RUN apk add --no-cache \
    automake \
    g++ \
    git \
    make \
    musl-dev \
    py3-pip \
    python3-dev

WORKDIR /opt/app

# Refresh the old CPU detection scripts before configuring MeCab.
RUN git clone -q https://github.com/taku910/mecab.git /opt/mecab \
  && cd /opt/mecab/mecab \
  && cp /usr/share/automake-*/config.guess ./config.guess \
  && cp /usr/share/automake-*/config.sub ./config.sub \
  && ./configure --enable-utf8-only --with-charset=utf8 \
  && make > /dev/null \
  && make install \
  && rm -rf /opt/mecab/

COPY requirements.txt ./
RUN python3 -m venv /venv \
  && . /venv/bin/activate \
  && pip install --no-cache-dir -r requirements.txt \
  && python3 -m unidic download

COPY app.py /opt/app/
RUN adduser -D nonroot
USER nonroot

# Validate the native extension and full UniDic dictionary on each target CPU.
RUN /venv/bin/python -c "from app import parseText; assert parseText('麩菓子', None)"

EXPOSE 8000
CMD ["/venv/bin/gunicorn", "-b", "0.0.0.0", "app"]
