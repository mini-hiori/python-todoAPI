new Vue({
    el: '.todoapi',
    data: {
        is_login_success: false,
        idtoken: '',
        searched_task: {},
        selectedtask: [],
        manual_task_name: '',
        manual_description: ''
    },
    methods: {
        update_task: function () {
            let self = this;
            const data = {
                "task_id": self.selectedtask[0],
                "task_name":self.manual_task_name,
                "description":self.manual_description
            }
            if (self.manual_task_name && self.manual_description && self.selectedtask.length === 1) {
                $.ajax({
                    url: "https://python-todoapi.mini-hiori.info/update_task", // 通信先のURL
                    type: "POST",
                    data: JSON.stringify(data),
                    dataType:"json",
                    headers: {
                        'Authorization': self.idtoken,
                        'Content-Type': 'application/json'
                      },
                    }).done(function(data1,textStatus,jqXHR) {
                        alert("TODO編集成功");
                        self.scan_task();
                    }).fail(function(jqXHR, textStatus, errorThrown){
                        alert("検索結果がありません");
                    });
            } else {
                alert("更新対象のTODOを1つだけ選択して、task_nameとdescriptionを入力してください");
            }
        },
        create_task: function () {
            let self = this;
            const data = {
                "task_name":self.manual_task_name,
                "description":self.manual_description
            }
            if (self.manual_task_name && self.manual_description) {
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
                        alert("TODO追加成功");
                        self.scan_task();
                    }).fail(function(jqXHR, textStatus, errorThrown){
                        alert("検索結果がありません");
                    });
                } else {
                    alert("task_nameとdescriptionを入力してください");
                }
        },
        delete_task: function () {
            let self = this;
            if (self.selectedtask.length > 0) {
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
                            alert("削除成功");
                            self.scan_task();
                        }).fail(function(jqXHR, textStatus, errorThrown){
                            alert("検索結果がありません");
                        });
                });
            } else {
                alert("削除したいtaskを1つ以上選択してください");
            }
        },
        search_task: function () {
            let self = this;
            if (!self.manual_task_name) {
                self.scan_task();
            } else {
                $.ajax({
                    url: "https://python-todoapi.mini-hiori.info/search_task?task_name=" + self.manual_task_name, // 通信先のURL
                    type: "GET",
                    dataType:"json",
                    headers: {
                        'Authorization': self.idtoken,
                        'Content-Type': 'application/json'
                    },
                    }).done(function(data1,textStatus,jqXHR) {		
                        alert("検索成功");
                        self.searched_task = data1;
                        self.selectedtask = [];
                    }).fail(function(jqXHR, textStatus, errorThrown){
                        alert("検索結果がありません");
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
                            self.searched_task = data1;
                            self.selectedtask = [];
                }
            })
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
                    alert("ログイン成功");
                    self.is_login_success = true;
                    console.log(self.idtoken);
                    self.scan_task();
                },
        
                onFailure: function(err) {
                    alert(err.message || JSON.stringify(err));
                    return "";
                },
            });
      }
    }
  });
