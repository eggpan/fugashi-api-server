# fugashi-api-server

[fugashi](https://github.com/polm/fugashi) を利用したAPIサーバ

## Usage

Herokuで実行する場合

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/eggpan/fugashi-api-server)

直接実行する場合

```bash
git clone https://github.com/eggpan/fugashi-api-server.git
cd fugashi-api-server
pip3 install -r requirements.txt
python3 -m unidic download
gunicorn app
```

Dockerを利用する場合

```bash
docker run -d -p 8000:8000 eggpan/fugashi-api-server
```

---

`text` をGETパラメータとして渡すと、JSONが帰ってきます。  
http://localhost:8000?text=麩菓子は、麩を主材料とした日本の菓子。
