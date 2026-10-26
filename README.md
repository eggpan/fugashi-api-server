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

`linux/amd64` と `linux/arm64` に対応し、実行環境に合ったイメージが自動選択されます。

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

### Docker Hubへの自動公開

GitHub Actionsで `main` ブランチまたはタグへのpush時に、amd64/arm64両対応の
`eggpan/fugashi-api-server` イメージをビルドしてDocker Hubに公開します。
`main` 向けのプルリクエストでは両アーキテクチャのビルド確認だけを実行します。
各ビルドで、実行ユーザーによるfugashiとUniDicの読み込み・形態素解析も確認します。

事前にDocker Hubの `eggpan/fugashi-api-server` リポジトリを用意し、
GitHubリポジトリの Settings → Secrets and variables → Actions に次のRepository secretsを登録してください。

| Secret | 値 |
| --- | --- |
| `DOCKERHUB_USERNAME` | Docker Hubのユーザー名（`eggpan` にpushする権限が必要） |
| `DOCKERHUB_TOKEN` | 対象リポジトリへの書き込み権限を持つDocker Hubアクセストークン |

| push先 | 公開されるDockerタグ |
| --- | --- |
| `main` | `main`, `latest` |
| `v1.2.3` などのGitタグ | Gitタグと同じ名前（例: `v1.2.3`） |

Gitタグの `/` など、Dockerタグに使用できない文字は `-` に変換されます。
タグのpushでは `latest` を更新しません。

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
