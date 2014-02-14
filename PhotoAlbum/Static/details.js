var pagenum;

$(document).ready(function() {	
	recalculatesum()
})

function recalculatesum() {
	$("#sum").val((pagenum * 5 * $("#quantity").val()));
	$("#suminput").text((pagenum * 5 * $("#quantity").val()) + " €");
}

function checkfields() {
	var valid = true;
	$("td").children().each(function () {
		if ($(this).is("input") && $(this).val() == ""){
			valid = false;
		}
	})
	
	if (!valid) {
		alert("Please fill all fields!");
		return false;
	}
	
	return true
}