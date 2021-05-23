new Vue({
    el: '.todoapi',
    data: {
        idtoken: '',
        searched_task: {},
        selectedtask: []
    },
    methods: {
        create_task: function () {
            let self = this;
            var task_name = document.getElementById("manual_task_name").value;
            var description = document.getElementById("manual_description").value;
            const data = {
                "task_name":task_name,
                "description":description
            }
            if (task_name && description) {
                $.ajax({
                    url: "https://python-todoapi.mini-hiori.info/create_task", // 通信先のURL
                    type: "PUT",
                    data: JSON.stringify(data),
                    dataType:"json",
                    headers: {
                        'Authorization': self.idtoken,
                        'Content-Type': 'application/json'
                      },
                    }).done(function(data1,textStatus,jqXHR) {		
                            if (jqXHR.status === 200) {
                                alert("TODO追加成功");
                            } else {
                                alert("検索結果がありません");
                            }
                    });
                }
        },
        delete_task: function () {
            let self = this;
            self.selectedtask.forEach(task_id => {
                $.ajax({
                    url: "https://python-todoapi.mini-hiori.info/delete_task?task_id=" + task_id, // 通信先のURL
                    type: "DELETE",
                    dataType:"json",
                    headers: {
                        'Authorization': self.idtoken,
                        'Content-Type': 'application/json'
                      },
                    }).done(function(data1,textStatus,jqXHR) {		
                            if (jqXHR.status === 200) {
                                alert("削除成功:" + task_id);
                            } else {
                                alert("検索結果がありません");
                            }
                    });
            });
        },
        search_task: function (task_name) {
            let query = "";
            if (task_name) {
                query = "?task_name=" + task_name
            }
            let self = this;
            alert(self.idtoken);
            $.ajax({
                url: "https://python-todoapi.mini-hiori.info/search_task" + query, // 通信先のURL
                type: "GET",
                dataType:"json",
                headers: {
                    'Authorization': self.idtoken,
                    'Content-Type': 'application/json'
                  },
                }).done(function(data1,textStatus,jqXHR) {		
                        if (jqXHR.status === 200) {
                            alert("検索成功");
                            self.searched_task = data1;
                            console.log(self.searched_task);   
                        } else {
                            alert("検索結果がありません");
                        }
                });
        },
        authorization: function() {
            let self = this;
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
            cognitoUser.authenticateUser(authenticationDetails, {
                onSuccess: function(result) {
                    self.idtoken = result.getIdToken().getJwtToken();          // IDトークン
        
                    console.log("idToken : " + self.idtoken);
                    alert("ログイン成功");
                },
        
                onFailure: function(err) {
                    alert(err.message || JSON.stringify(err));
                    return "";
                },
            });
      }
    }
  });