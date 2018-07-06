let index_of_image = 0;
function changeImg(){
	let img = document.getElementById("bannerV2");

	//计算出当前要切换到第几张图片
	let curIndex = index_of_image%2 + 1;  //1,2
	img.style='background:url(../static/image/'+curIndex+'.jpg) 50% 50% no-repeat;background-size: cover;height:850px;';

	//每切换完,索引加1
	index_of_image = index_of_image + 1;
}

//	获取元素对象
function g(id){
    return document.getElementById(id);
}

function init(){
	setInterval("changeImg()",3000);
}

//	自动居中元素
function autoCenter( el ){
	let bodyW = document.documentElement.clientWidth;
	let bodyH = document.documentElement.clientHeight;

	let elW = el.offsetWidth;
	let elH = el.offsetHeight;

	el.style.left = (bodyW-elW)/2 + 'px';
	el.style.top = (bodyH-elH)/2 + 'px';
}

//	自动扩展元素到全部显示区域
function fillToBody( el ){
	el.style.width  = document.documentElement.clientWidth  +'px';
	el.style.height = document.documentElement.clientHeight + 'px';
}

//	重新调整对话框的位置和遮罩，并且展现
function showDialog(){
	g('dialog_login').style.display = 'block';
	g('search').style.display = 'none';
}

function showDialogContact(){
	g('dialog_contact').style.display = 'block';
	g('search').style.display = 'none';
}
