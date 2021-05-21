# python-todoAPI
todoを登録するREST API

## 構成図
![](https://raw.githubusercontent.com/mini-hiori/python-todoAPI/main/docs/architecture.png)

## DynamoDBテーブル定義

| user_id(PK) | task_id(SK) | task_name(LSI) | description | created_at | updated_at | 
| ---- | ---- | ---- | ---- | ---- | ---- |
| mini-hiori | 012... | Zennに記事書く | TS×ffmpegの話 | 20210401 | 20210601 | 
| mini-hiori | 345... | AWSSummit出る | 特にコナミの事例が気になる | 20210501 | 20210501 |
| mini-koharu | 678... | 買い出し | 水がない | 20210301 | 20210404 |
| mini-koharu | 90... | 家の掃除 | ダンボールが… | 20210401 | 20210501 |

- task_idは[uuid.uuid4()](https://dev.classmethod.jp/articles/how-generate-uuid-python-uuid4/)により生成する
- user_idはCognitoのユーザー名をそのまま用いる

## API仕様書
[こちら](https://mini-hiori.github.io/python-todoAPI/)

## 環境構築
- serverless frameworkを利用して以下を作成する
    - Lambda(コンテナイメージ利用)
    - API Gateway
    - DynamoDB
- 以下は手動で作成
    - ECR
    - Cognito+APIGatewayのCognitoオーソライザー設定
    - Route53、APIGatewayのカスタムドメイン設定
    - ACMの証明書

## デプロイ
- Github Actionsによりmainブランチへのpush時にECRへのpushが走る
    - [元ネタ](https://dev.classmethod.jp/articles/github-action-ecr-push/)

## テスト
- testディレクトリ内にテストケースに対応するファイルが記載されている
    - Cognito+APIGatewayの認証が機能しているか
    - 各種エンドポイントを利用してtaskの追加/削除/検索/更新ができるか
    - パラメータミス等で検索結果や変更対象になるtaskがないときに400エラーを返せるか
- pytestコマンドで一括実行できる

## 認証/認可
- Cognitoの認証結果のIDトークンを渡されなければAPIを利用できない
    - APIGateway内のオーソライザー設定による
- トークンが渡されたら、API内でトークンを解析してCognitoのユーザーIDを得る
    - このユーザーIDをパーティションキーとして利用することで、ログインユーザー以外のtaskの操作の制限を実現している