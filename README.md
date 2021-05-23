# python-todoAPI
todoを登録するREST API

## テスト
[こちら](https://mini-hiori.github.io/python-todoAPI/gui.html)
- todoアプリのフロントエンドをVue.js+bootstrapで作成し、Github Pagesでホストしている
    - Cognitoに登録済みのユーザーでログインでき、ユーザー単位でtask操作可能

## API仕様書
[こちら](https://mini-hiori.github.io/python-todoAPI/)
- OpenAPI(yaml)形式で記載したものを[redoc-cli](https://lunaticsol.wordpress.com/2020/05/18/generate-html-from-swagger-json-by-redoc-cli/)でhtml化しGithub Pagesでホストしている

## 構成図
![](https://raw.githubusercontent.com/mini-hiori/python-todoAPI/main/docs/architecture.png)
- 維持コストがかからない点でサーバーレス構成を選択
- 認証もマネージドに行いたいのでCognitoを利用
    - もしCognitoを使わないなら別途DynamoDB or RDSでユーザー情報を管理することになりそう

## 環境構築
- serverless frameworkを利用して以下を作成する
    - Lambda
    - API Gateway
    - DynamoDB
- 以下は手動で作成
    - ECR
    - Cognito
    - Route53(DNSレコード設定)
    - ACMの証明書
    - APIGatewayの各種設定
        - Cognitoオーソライザー
        - カスタムドメイン
        - CORS許可

## Lambda
- コンテナイメージで動作
- Pythonをベースに[FastAPI](https://fastapi.tiangolo.com/ja/)と[Mangum](https://github.com/jordaneremieff/mangum)を利用している
    - プログラムを一切変えずにコンテナアプリケーションとしても動作させることができる点がメリット。  
    FargateやAppRunnerで動かしたくなったときもDockerfileの修正のみで対応可能
    - FastAPIはドキュメント生成機能があるため運用フレンドリー

## DynamoDBテーブル定義

| user_id(PK) | task_id(SK) | task_name(LSI) | description | created_at | updated_at | 
| ---- | ---- | ---- | ---- | ---- | ---- |
| mini-hiori | 012... | Zennに記事書く | TS×ffmpegの話 | 20210401 | 20210601 | 
| mini-hiori | 345... | AWSSummit出る | 特にコナミの事例が気になる | 20210501 | 20210501 |
| mini-koharu | 678... | 買い出し | 水がない | 20210301 | 20210404 |
| mini-koharu | 90... | 家の掃除 | ダンボールが… | 20210401 | 20210501 |

- task_idは[uuid.uuid4()](https://dev.classmethod.jp/articles/how-generate-uuid-python-uuid4/)により生成する
- user_idはCognitoのユーザー名をそのまま用いる
- task_nameで検索がしたいはずなのでLSIをtask_nameに設定

## 認証/認可
- Cognitoの認証結果のIDトークンを渡されなければAPIを利用できない
    - APIGateway内のオーソライザー設定による
- トークンが渡されたら、API内でトークンを解析してCognitoのユーザーIDを得る
    - このユーザーIDをパーティションキーとして検索等に利用することで、ログインユーザー以外のtaskの操作の制限を実現している

## デプロイ
- Github Actionsによりmainブランチへのpush時にECRへのpushが走る
    - [元ネタ](https://dev.classmethod.jp/articles/github-action-ecr-push/)

## テスト
- testディレクトリ内にテストケースに対応するファイルが記載されている
    - Cognito+APIGatewayの認証が機能しているか
    - 各種エンドポイントを利用してtaskの追加/削除/検索/更新ができるか
    - パラメータミス等で検索結果や変更対象になるtaskがないときに400エラーを返せるか
- pytestコマンドで一括実行できる

## 課題
- Dockerfileが重い
    - プレーンなalpineに必要なものをインストールして…とやっているせい
    - AWS公式のlambda用イメージを使った方がビルドが早いが、VSCode Remote Containerでうまく動いていない
- Lambdaのデプロイイメージの差し替えが手動
- WAF、Usage Plan(APIGaetway)等の使用によるアクセス制限
    - ログインIDを知っていれば多分APIを壊せてしまう
- DynamoDBの結果整合性の考慮
    - APIのオプションで強い整合性の読み込みを強制するとかしてもよかった
- 自動テストをmainへのマージ前のチェックとして仕込む
    - Linterも仕込める余地がある
- serverless frameworkの活用
    - 少なくともCORS許可はserverless.yml内に書き込める
- ユーザーのサインアップやメール検証を行うAPI/フロントが欲しい
- テストサイトをGithub Pages→S3+CloudFrontにしたい
    - 純粋な技術的興味。コスト的にはPagesの方が良い
    - 他にもTypeScriptとかReactとか… そもそも単一componentだとグローバル変数一辺倒になってしまってスマートではない