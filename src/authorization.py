import base64
import json
import traceback


def decode_base64url(string: str) -> str:
    # https://qiita.com/c-yan/items/7eee72ad8eaa0f441017
    return base64.urlsafe_b64decode(string + b"=" * ((4 - len(s) & 3) & 3)).decode()


def get_userid_from_idtoken(id_token: str) -> str:
    """
    cognitoのidトークンを検証してユーザーIDを得る
    ※cognitoのidトークンはjson web tokenなので、.で区切ってbase64urlでデコードするとユーザー情報が得られる
    """
    if not id_token:
        return ""
    try:
        user_id = json.loads(decode_base64url(id_token.split(".")[1].encode()))[
            "cognito:username"
        ]
        return user_id
    except BaseException:
        print(traceback.format_exc())
        return ""
