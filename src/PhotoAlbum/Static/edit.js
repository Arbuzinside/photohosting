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
				if (index) {
					applylayout(index);
					$(this).dialog( "close" );
				} 
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
				var cap = $('input[name=piccaption]').val();
				if (url && cap) {
					uploadimage(url, cap);
					$(this).dialog( "close" ); 
				}
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
			'<div id="allpanel'+ page +'" class="imageholder"></div> '
		);
	}
	else if (index == 2) {
		$("#" + pagetoload).html(
			'<div id="toppanel'+ page +'" class="imageholder"></div> \
			<div id="bottompanel'+ page +'" class="imageholder"></div> '
		);
	}
	else if (index == 3) {
		$("#" + pagetoload).html(
			'<div id="leftpanel'+ page +'" class="imageholder"></div> \
			<div id="rightpanel'+ page +'" class="imageholder"></div> \
			<div id="toppanel'+ page +'" class="imageholder"></div> '
		);
	}
	else if (index == 4) {
		$("#" + pagetoload).html(
			'<div id="toppanel'+ page +'" class="imageholder"></div> \
			<div id="leftpanel'+ page +'" class="imageholder"></div> \
			<div id="rightpanel'+ page +'" class="imageholder"></div>'
		);
	}
	
	$(".imageholder").click(function (event) {
		imageplace = event.target.id;
		page = imageplace[imageplace.length - 1];
		
		$('input[name=picurl]').val('');	// clear textboxes
		$('input[name=piccaption]').val('');
		$('#uploadpic').dialog("open");		// pops up dialog to enter picture url
	});
}

function uploadimage (url, cap) {				// display picture: url and caption
	side = page == 0 ? "leftpage" : "rightpage";
	$("#" + side).find("#" + imageplace).html(
		'<figure> \
			<img alt="' + url + '" src="' + url + '" > \
			<figcaption>'+ cap +'</figcaption> \
		</figure>'
	);
	$("#" + side).find("#" + imageplace).css("background-image", "none");
}

function deletelayout(num)
{
	page = num;
	side = page == 0 ? "leftpage" : "rightpage";
	$("#" + side).html("");
	$("#" + side).css("background-image", "url('/Static/images/layout.png')");
	$("#" + side).css("cursor", "pointer");
	
	if (side == "leftpage") {
		$("#leftpage").on("click", function () {
			$('#dialog').dialog("open");
			page = 0;
		})
	}
	else {
		$("#rightpage").on("click", function () {
			$('#dialog').dialog("open");
			page = 1;
		})
	}
}
	