$().ready(function(){
 $("#signupinform").validate({
   rules:{
     user_sign: {
       required: true,
       maxlength: 10
     },

     pass_sign: {
        required: true,
        minlength: 2,
        maxlength: 20
     },

     pass_repeat: {
       required: true,
       minlength: 2,
       maxlength: 20,
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
       maxlength: "用户名必须由10个以下字符组成"
     },
     pass_sign: {
        required: "请输入密码",
        minlength: "密码长度不能小于2个字符",
        maxlength: "密码长度不能大于2个字符"
     },

     pass_repeat: {
       required: "请输入密码",
       minlength: "密码长度不能小于2个字符",
       maxlength: "密码长度不能大于20个字符",
       equalTo: "两次密码输入不一致"
     },

     email: {
       required: "请输入邮箱",
       email: "请输入一个正确格式的邮箱"
     }
   }
 })
});