# fugashi-api-server

[fugashi](https://github.com/polm/fugashi) を利用した、形態素解析を行うAPIサーバ

## Usage

### Herokuで実行する場合
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/eggpan/fugashi-api-server)

### Renderで実行する場合
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/eggpan/fugashi-api-server)

### Dockerを利用する場合
```bash
docker run -d -p 8000:8000 eggpan/fugashi-api-server
```

ローカルでビルドする場合:

```bash
docker build -t fugashi-api-server .
docker run --rm -p 8000:8000 fugashi-api-server
```

Alpine 3.24と、同ブランチで提供されるPython 3.14を使用します。
Pythonの依存ライブラリは `requirements.txt` でバージョンを固定しています。
MeCabをビルドする際、`./configure` の前に `config.guess` と `config.sub` を
Alpineのautomakeパッケージに含まれる版へ更新し、arm64を認識できるようにしています。
UniDicの辞書はビルド時にダウンロードするため、インターネット接続と十分な空き容量が必要です。

### 直接実行する場合
```bash
git clone https://github.com/eggpan/fugashi-api-server.git
cd fugashi-api-server
pip3 install -r requirements.txt
python3 -m unidic download
gunicorn app
```

---

`text` をGETパラメータとして渡すと、JSONが帰ってきます。

デモ  
https://fugashi-api-server-vchq.onrender.com/?text=麩菓子は、麩を主材料とした日本の菓子。
