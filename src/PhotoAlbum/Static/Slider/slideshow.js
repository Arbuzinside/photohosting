/*$(function() {
    $('.banner').unslider();
});*/
$(document).ready(function() {
	$(".above").fadeOut();
})

function slider() {
	$(".above").fadeToggle(2000);
	$(".below").fadeToggle(2000);
}
setInterval(function(){ slider(); }, 5000);