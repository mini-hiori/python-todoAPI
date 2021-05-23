async function search_task() {

    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    let UserPoolId = document.getElementById("userpoolid").value;
    let AppClientId = document.getElementById("appclientid").value;

    var authenticationData = {
        Username: username,
        Password: password,
    };

    var authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails(
        authenticationData
    );
    var poolData = {
        UserPoolId: UserPoolId, // Your user pool id here
        ClientId: AppClientId, // Your client id here
    };
    var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
    var userData = {
        Username: username,
        Pool: userPool,
    };

    var cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
    let idtoken = await cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: function(result) {
            var idToken = result.getIdToken().getJwtToken();          // IDトークン
            var accessToken = result.getAccessToken().getJwtToken();  // アクセストークン
            var refreshToken = result.getRefreshToken().getToken();   // 更新トークン

            console.log("idToken : " + idToken);
            console.log("accessToken : " + accessToken);
            console.log("refreshToken : " + refreshToken);
            call_search_api(idToken,"test_");
        },

        onFailure: function(err) {
            alert(err.message || JSON.stringify(err));
            return "";
        },
    });
    return idtoken;
}

function call_search_api(token,task_name) {
	console.log("token:" + token);
    $.ajax({
        url: "https://python-todoapi.mini-hiori.info/search_task?task_name=" + task_name, // 通信先のURL
        type: "GET",
		dataType:"json",
		headers: {
			'Authorization': token,
			'Content-Type': 'application/json'
		  },
        }).done(function(data1,textStatus,jqXHR) {		
                // 4. JavaScriptオブジェクトをJSONに変換
                if (jqXHR === 200) {
					var result_data = JSON.stringify(data1);
					alert("検索成功");
					console.log(result_data);
				} else {
					alert("検索結果がありません");
				}
        });
}