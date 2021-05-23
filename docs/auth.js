async function OnCognitoAuthenticateUser() {

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
            alert("ログイン成功");
            return idToken;
        },

        onFailure: function(err) {
            alert(err.message || JSON.stringify(err));
            return "";
        },
    });
    return idtoken;
}