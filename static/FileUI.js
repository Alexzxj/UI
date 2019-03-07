/**
 * Created by T470P on 2019/2/2.
 */
var FileUI = { };
 FileUI.Tool = {
     ajax: function (url, para) {
         return new Promise(function (resolve, reject) {
             $.ajax({
                 type: "post",
                 url: url,
                 data: para,
                 contentType: "application/json",
                 dataType: "json",
             }).then(function (resp) {
                 resolve(resp);
             }, function (error) {
                 reject(error);
             });
         });
     }
 };
  FileUI.Action = {
      saveProject: function () {
          var _val = $("#txtProject").val();
          console.log(_val)
          if (_val === "") {
              alert("创建项目不能为空！！");
              return;
          }
          var action = $("#actionProject").attr("name");
          switch (action) {
              case "add":
                  var para = JSON.stringify({val: _val});
                  FileUI.Tool.ajax("/add", para).then(function (resp) {
                      if (resp.errorCode == 0) {
                          // 正确
                          alert(resp.errorMsg);
                          location.reload();
                      } else if (resp.errorCode == -1) {
                          alert("创建项目不存在！！");
                      } else {
                          alert("输入项目已经存在！！");
                      }
                  }).catch(function (error) {
                      // 代码错误，网络异常
                      console.log(error);
                  })
                  break;
              case "edit":
                  var key = $("#current").attr("name");
                  var para = JSON.stringify({val: _val, "key": key});
                  FileUI.Tool.ajax("/edit", para).then(function (resp) {
                      if (resp.errorCode == 0) {
                          // 正确
                          alert(resp.errorMsg);
                          location.reload();
                      } else if (resp.errorCode == -1) {
                          alert("创建项目不存在！！");
                      } else {
                          alert("输入项目已经存在！！");
                      }
                  }).catch(function (error) {
                      // 代码错误，网络异常
                      console.log(error);
                  })
                  break;
              case "del":
                  if (confirm("删除项目时,对应的文件也会跟着删除,此操作不可逆,确认删除吗？")) {
                      var key = $("#current").attr("name");
                      var para = JSON.stringify({"val": key});
                      FileUI.Tool.ajax("/delProject", para).then(function (resp) {
                          if (resp.errorCode == 0) {
                              // 正确
                              alert(resp.errorMsg);
                              location.reload();
                          } else if (resp.errorCode == -1) {
                              alert("创建项目不存在！！");
                          } else {
                              alert("输入项目已经存在！！");
                          }
                      })
                  }
                  break;
          }
      },
      addProject: function () {
          $("#projectContene").show();
          $("span[name='tip']").html("当前操作:<font style='color: red'>创建</font>")
          $("#actionProject").attr("name", "add");

      }, editProject: function () {
          FileUI.Action.verifProject("edit");
          $("span[name='tip']").html("当前操作:<font style='color: red'>修改</font>")
          var _val = $("select[name='ST_TYPE']");
          $("#current").attr("name", _val.val())
      }, delProject: function () {
          FileUI.Action.verifProject("del");
          $("span[name='tip']").html("当前操作:<font style='color: red'>删除</font>")
          var _val = $("select[name='ST_TYPE']");
          $("#current").attr("name", _val.val())
      }, verifProject: function (type) {
          $("#projectContene").show();
          var _val = $("select[name='ST_TYPE']");
          $("#txtProject").val(_val.find("option:selected").text());
          if (_val === "") {
              alert("所属项目不能为空！！");
              return;
          }
          $("#actionProject").attr("name", type)
      }, listUIFile: function () {
          //$("#projectContene").hide();
          var _val = $("select[name='ST_TYPE']");
          location.href = '/index/dir=./ui/' + _val.find("option:selected").text() + '/';
      }, delUIFile: function (evt) {
          if (confirm("删除文件时,用户不能正常预览,确认删除吗？")) {
              var _name = $(evt).attr('name');
              $.ajax({
                  url: '/del',
                  type: 'post',
                  dataType: 'json',
                  data: JSON.stringify({
                      val: _name
                  }),
                  success: function (res) {
                      if (res.errorCode == 0) {
                          alert('删除成功');
                          location.reload();
                      } else {
                          alert(res.error_msg || '删除失败');
                      }
                  }
              })
          }
      }, downloadAllFile: function () {  //一键下载
          var _val = $("select[name='ST_TYPE']");
          _name = _val.find("option:selected").text();
          $.ajax({
              url: '/downloadAllFile',
              type: 'post',
              dataType: 'json',
              data: JSON.stringify({
                  val: _name
              }),
              success: function (res) {
                  if (res.errorCode == 0) {
                      window.open("http://"+res.request.ip+":5556/"+res.request.url);
                  } else {
                      alert(res.error_msg || '删除失败');
                  }
              }
          })
      },listZip: function (event) {
          var val = $(event).find('option:selected').attr('data-name');
          location.href = '/history/dir=./file/' + val + '/';
      },downloadZip: function (evt) {  //
          var _name = $(evt).attr('name');
          $.ajax({
              url: '/downloadZip',
              type: 'post',
              dataType: 'json',
              data: JSON.stringify({
                  val: _name
              }),
              success: function (res) {
                  if (res.errorCode == 0) {
                      window.open("http://"+res.request.ip+":5556/"+res.request.url);
                  } else {
                      alert(res.error_msg || '删除失败');
                  }
              }
          })
      }, delUIZip: function (evt) {
          if (confirm("删除历史版本文件会彻底从服务器删除,此操作不可逆,确认删除吗？")) {
              var _name = $(evt).attr('name');
              $.ajax({
                  url: '/delZip',
                  type: 'post',
                  dataType: 'json',
                  data: JSON.stringify({
                      val: _name
                  }),
                  success: function (res) {
                      if (res.errorCode == 0) {
                          alert('删除成功');
                          location.reload();
                      } else {
                          alert(res.error_msg || '删除失败');
                      }
                  }
              })
          }
      }
  };