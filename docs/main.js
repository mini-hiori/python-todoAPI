new Vue({
    el: '.todoapi',
    data: {
        is_login_success: false,
        idtoken: '',
        searched_task: {},
        selectedtask: []
    },
    methods: {
        update_task: function () {
            let self = this;
            let task_name = document.getElementById("manual_task_name").value;
            let description = document.getElementById("manual_description").value;
            const data = {
                "task_name":task_name,
                "description":description
            }

            if (task_name && description && selectedtask.length == 1) {
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
            } else {
                alert("更新対象のTODOを1つだけ選択して、task_nameとdescriptionを入力してください");
            }
        },
        create_task: function () {
            let self = this;
            let task_name = document.getElementById("manual_task_name").value;
            let description = document.getElementById("manual_description").value;
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
        search_task: function () {
            let self = this;
            let task_name = document.getElementById("manual_task_name").value;
            if (task_name) {
                self.scan_task();
            } else {
                $.ajax({
                    url: "https://python-todoapi.mini-hiori.info/search_task?task_name=" + task_name, // 通信先のURL
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
                }
        },
        scan_task: function () {
            let self = this;
            $.ajax({
                url: "https://python-todoapi.mini-hiori.info/scan_task", // 通信先のURL
                type: "GET",
                dataType:"json",
                headers: {
                    'Authorization': self.idtoken,
                    'Content-Type': 'application/json'
                  },
                }).done(function(data1,textStatus,jqXHR) {		
                        if (jqXHR.status === 200) {
                            alert("TODO取得成功");
                            self.searched_task = data1;
                            console.log(self.searched_task);   
                        } else {
                            alert("検索結果がありません");
                        }
                });
        },
        authorization: function() {
            let self = this;
            let username = document.getElementById("username").value;
            let password = document.getElementById("password").value;
        
            let UserPoolId = document.getElementById("userpoolid").value;
            let AppClientId = document.getElementById("appclientid").value;
        
            let authenticationData = {
                Username: username,
                Password: password,
            };
        
            let authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails(
                authenticationData
            );
            let poolData = {
                UserPoolId: UserPoolId, // Your user pool id here
                ClientId: AppClientId, // Your client id here
            };
            let userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
            let userData = {
                Username: username,
                Pool: userPool,
            };
        
            let cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
            cognitoUser.authenticateUser(authenticationDetails, {
                onSuccess: function(result) {
                    self.idtoken = result.getIdToken().getJwtToken();          // IDトークン
        
                    console.log("idToken : " + self.idtoken);
                    alert("ログイン成功");
                    self.is_login_success = true;
                },
        
                onFailure: function(err) {
                    alert(err.message || JSON.stringify(err));
                    return "";
                },
            });
      }
    }
  });