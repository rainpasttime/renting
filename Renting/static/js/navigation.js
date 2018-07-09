//	获取元素对象
function g(id){
    return document.getElementById(id);
}

//	重新调整登录注册对话框的位置和遮罩，并且展现
function showDialog(){
	g('dialog_login').style.display = 'block';
	g('search').style.display = 'none';
}

//联系我们的弹出框
function showDialogContact(){
	g('dialog_contact').style.display = 'block';
	g('search').style.display = 'none';
}

let new_scroll_position = 0;
let last_scroll_position;
let header = document.getElementById("header");

window.addEventListener('scroll', function(e) {
  last_scroll_position = window.scrollY;

  // 向下滚动
  if (new_scroll_position < last_scroll_position && last_scroll_position > 80) {
    header.classList.remove("slideDown");
    header.classList.add("slideUp");

  // 向上滚动
  } else if (new_scroll_position > last_scroll_position) {
    header.classList.remove("slideUp");
    header.classList.add("slideDown");
  }

  new_scroll_position = last_scroll_position;
});