$(document).ready(function(){ 
	$('.albumcontrollers').hide();
	
	$('.albumimg').hover(function () {
		var actid = this.id.split('.');
		$("#contr\\." + actid[1]).show();
	});
	
	$('.albumcontrollers').hover(function () {
		var actid = this.id.split('.');
		$("#contr\\." + actid[1]).show();
	});
	
	$('.albumimg').mouseleave(function () {
		var actid = this.id.split('.');
		$("#contr\\." + actid[1]).hide();
	});
	
	$('.albumcontrollers').mouseleave(function () {
		var actid = this.id.split('.');
		$("#contr\\." + actid[1]).hide();
	});
});