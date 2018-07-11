window.onload = function () {
    let oxx = document.getElementById('xx');
    let obanner = document.getElementById('top-banner');
    let otext = document.getElementById('textt');
}

$(document).ready(function () {
    //手动控制轮播图
    $('#one li').eq(0).show();

    $('#two li').mouseover(function () {
        $(this).addClass('on').siblings().removeClass('on');
        let index = $(this).index();
        i = index;
        // $('#one li').eq(index).stop().fadeIn(300).siblings().stop().fadeOut(300);
        $('#one li').eq(i).addClass('on').siblings().removeClass('on');
    })


    let len = $("#two li").length;
    //自动播放
    let i = 0;
    let t = setInterval(move, 4000);
    //自动播放核心函数
    function move() {
        i++;
        if (i == len) {
            i = 0;
        }
        $('#two li').eq(i).addClass('on').siblings().removeClass('on');
        // $('#one li').eq(i).fadeIn(300).siblings().fadeOut(300);
        $('#one li').eq(i).addClass('on').siblings().removeClass('on');
    }

    //向右播放核心函数
    function moveL() {
        i--;
        if (i == -1) {
            i = len - 1;
        }

        $('#two li').eq(i).addClass('on').siblings().removeClass('on');
        // $('#one li').eq(i).fadeIn(300).siblings().fadeOut(300);
        $('#one li').eq(i).addClass('on').siblings().removeClass('on');
    }


    $('#left').click(function () {
        moveL();
    })

    $('#right').click(function () {
        move();
    })

    //鼠标移入移除
    $('#lunbo').hover(function () {
        clearInterval(t);
    }, function () {
        t = setInterval(move, 4000);
    })

})