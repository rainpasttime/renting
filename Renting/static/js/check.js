function picture_stop(obj,id){
	
		$(obj).parents("tr").find(".td-status").html('<span class="label label-defaunt radius" style="background-color: green;">已审核</span>');
		
}
function picture_del(obj,id){
		$(obj).parents("tr").find(".td-status").html('<span class="label label-success radius" style="background-color: gray;">未通过</span>');
		
}