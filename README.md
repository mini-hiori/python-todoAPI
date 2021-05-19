# python-todoAPI
todoを登録するREST API

## 構成図
![](https://raw.githubusercontent.com/mini-hiori/python-todoAPI/main/docs/architecture.png)

## DynamoDBテーブル定義

| user_id(PK) | task_id(SK) | task_name(LSI) | description | created_at | updated_at | 
| ---- | ---- | ---- | ---- | ---- | ---- |
| abc... | 012... | Zennに記事書く | TS×ffmpegの話 | 20210401 | 20210601 | 
| def... | 345... | AWSSummit出る | 特にコナミの事例が気になる | 20210501 | 20210501 |
| hij... | 678... | 買い出し | 水がない | 20210301 | 20210404 |
| klm... | 90... | 家の掃除 | ダンボールが… | 20210401 | 20210501 |

- task_idは[uuid.uuid4()](https://dev.classmethod.jp/articles/how-generate-uuid-python-uuid4/)により生成する
- user_idはCognitoの仕様による Python側で決められるならuuidで生成する

## API仕様書
[こちら](https://mini-hiori.github.io/python-todoAPI/)