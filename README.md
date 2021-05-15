# python-todoAPI
todoを登録するREST API

## 構成図
![](https://raw.githubusercontent.com/mini-hiori/python-todoAPI/main/docs/architecture.png)

## DynamoDBテーブル定義

| user_id(PK) | task_id(SK) | task_name(LSI) | description | created_at | 
| ---- | ---- | ---- | ---- | ---- |
| 1 | 0a00 | Zennに記事書く | TS×ffmpegの話 | 20210401 | 
| 1 | 01b2 | AWSSummit出る | 特にコナミの事例が気になる | 20210501 |
| 2 | 1amx | 買い出し | 水がない | 20210301 | 
| 2 | 2bms | 家の掃除 | ダンボールが… | 20210401 |