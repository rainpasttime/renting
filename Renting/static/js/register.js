$().ready(function(){
 $("#signupform").validate({
   rules:{
     user_sign: {
       required: true,
       minlength: 2,
       maxlength: 50
     },

     pass_sign: {
        required: true,
        minlength: 2,
        maxlength: 100
     },

     pass_repeat: {
       required: true,
       minlength: 2,
       maxlength: 100,
       equalTo: "#pass_sign"
     },

     email: {
       required: true,
       email: true
     }
   },
   messages: {
     user_sign: {
       required: "请输入用户名",
       minlength: "用户名必须由2个以上字符组成",
       maxlength: "用户名必须由50个以下字符组成"
     },
     pass_sign: {
        required: "请输入密码",
        minlength: "密码长度不能小于2个字符",
        maxlength: "密码长度不能大于100个字符"
     },

     pass_repeat: {
       required: "请输入密码",
       minlength: "密码长度不能小于2个字符",
       maxlength: "密码长度不能大于100个字符",
       equalTo: "两次密码输入不一致"
     },

     email: {
       required: "请输入邮箱",
       email: "请输入一个正确格式的邮箱"
     }
   }
 })

 $("#loginform").validate({
   rules:{
     user_login: {
       required: true,
       minlength: 2,
       maxlength: 50
     },

     pass_login: {
        required: true,
        minlength: 2,
        maxlength: 100
     }
   },
   messages: {
     user_login: {
        required: "请输入用户名",
        minlength: "用户名必须由2个以上字符组成",
        maxlength: "用户名必须由50个以下字符组成"
     },
     pass_login: {
        required: "请输入密码",
        minlength: "密码长度不能小于2个字符",
        maxlength: "密码长度不能大于100个字符"
     }
   }
 })

 $("#modify_form").validate({
   rules:{
     name_modify: {
       minlength: 2,
       maxlength: 50
     },
     password_modify: {
        minlength: 2,
        maxlength: 100
     },
     repeat_modify:{
        equalTo: "#password_modify"
     },
     email_modify:{
        email: true
     },
     phone_modify:{
        digits:true
     }
   },
   messages: {
     name_modify: {
       minlength: "名称最小2个字符",
       maxlength: "名称最多50个字符"
     },
     password_modify: {
        minlength: "密码最小2个字符",
        maxlength: "密码最多100个字符"
     },
     repeat_modify:{
        equalTo: "两次密码不一致"
     },
     email_modify:{
        email: "请输入正确邮箱"
     },
     phone_modify:{
        digits:"请输入正确的阿拉伯数字"
     }
   }
 })
});