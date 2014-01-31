// Dialog window to add layouts
var page; // 0 = leftpage, 1 = rightpage
var imageplace;

$(document).ready(function() {

	// Add layout to the left page
	$('#leftpage').on("click", function () {
        $('#dialog').dialog("open");
		page = 0;	
    });
	
	// Add layout to the right page
	$('#rightpage').on("click", function () {
        $('#dialog').dialog("open");
		page = 1;	
    });
	
	$("#dialog").dialog({
		autoOpen: false,
		resizable: false,
		width: 600,
		modal: true,
		buttons: {
			Select: function() {
				var index = $('input[name=layoutselect]:checked').val();
				applylayout(index);
				$(this).dialog( "close" ); 
			}
		}
	});
	
	$("#uploadpic").dialog({
		autoOpen: false,
		resizable: false,
		width: 600,
		modal: true,
		buttons: {
			Select: function() {
				var url = $('input[name=picurl]').val();
				uploadimage(url);
				$(this).dialog( "close" ); 
			}
		}
	});
});

function applylayout(index) // index: selected layout index
{
	var pagetoload = page == 0 ? "leftpage" : "rightpage";
	$("#" + pagetoload).off();
	$("#" + pagetoload).hover().css("border", "1px dashed #333333");
	$("#" + pagetoload).css("background-image", "none");
	$("#" + pagetoload).css("cursor", "default");
	
	if (index == 1) {
		$("#" + pagetoload).html(
			'<div id="allpanel" class="imageholder"></div> '
		);
	}
	else if (index == 2) {
		$("#" + pagetoload).html(
			'<div id="toppanel" class="imageholder"></div> \
			<div id="bottompanel" class="imageholder"></div> '
		);
	}
	else if (index == 3) {
		$("#" + pagetoload).html(
			'<div id="leftpanel" class="imageholder"></div> \
			<div id="rightpanel" class="imageholder"></div> \
			<div id="toppanel" class="imageholder"></div> '
		);
	}
	else if (index == 4) {
		$("#" + pagetoload).html(
			'<div id="toppanel" class="imageholder"></div> \
			<div id="leftpanel" class="imageholder"></div> \
			<div id="rightpanel" class="imageholder"></div>'
		);
	}
	
	$(".imageholder").click(function (event) {
		imageplace = event.target.id;
		page = $("#" + imageplace).parent().attr('id') == "leftpage" ? 0 : 1;
		
		$('input[name=picurl]').val('');
		$('#uploadpic').dialog("open");		// pops up dialog to enter picture url
	});
}

function uploadimage (url) {				// display picture
	side = page == 0 ? "leftpage" : "rightpage";
	$("#" + side).find("#" + imageplace).html(
		'<img alt="' + url + '" src="' + url + '" >'
	);
	$("#" + side).find("#" + imageplace).css("background-image", "none");
}
	