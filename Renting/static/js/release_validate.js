$().ready(function(){
    $("#release_form").validate({
    rules:{
         house_name: {
              required: true,
              minlength: 4,
              maxlength: 25
         },
         area: {
              required: true,
              digits:true
         },
         people: {
              required: true,
              digits:true
         },
         bedroom: {
              required: true,
              digits:true
         },
         toilet: {
              required: true,
              digits:true
         },
         bed: {
               required: true,
               digits:true
         },
         description: {
               maxlength: 100
         },
         price: {
               required: true,
               digits:true
         },
         province: {
               required: true,
               maxlength:2
         },
         address: {
               required: true
         }
    },
    messages:{
         house_name: {
              required: "请输入房屋名字",
              minlength: "房屋名字不小于4个字",
              maxlength: "房屋名字不超过25个字"
         },
         area: {
              required: "请输入面积",
              digits:"面积必须是阿拉伯数字"
         },
         people: {
              required: "请输入可住人数",
              digits:"可住人数必须是阿拉伯数字"
         },
         bedroom: {
              required: "请输入卧室数",
              digits:"卧室数必须是阿拉伯数字"
         },
         toilet: {
              required: "请输入卫生间数目",
              digits:"卫生间数必须是数字"
         },
         bed: {
               required: "请输入床位数目",
               digits:"床位数必须是数字"
         },
         description: {
               maxlength: "房屋描述必须小于100个字"
         },
         price: {
               required: "请输入房屋价格",
               digits:"房屋价格必须是数字"
         },
         province: {
               required: "请输入省",
               maxlength:"省名不能超过2个字"
         },
         address: {
               required: "请输入具体地址"
         }
    }
 })
});