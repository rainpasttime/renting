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

