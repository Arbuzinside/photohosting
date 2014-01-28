$(document).ready(function() {

	// Dialog window to add layouts
	var page; // 0 = leftpage, 1 = rightpage
	$("#dialog").dialog({
		autoOpen: false,
		resizable: false,
		width: 300, //"auto"
		modal: true,
		buttons: {
			Select: function() {			
				//TODO: save the id of the layout
				if (page == 0) {
					$(leftpage).html(
						'<img src="/Static/images/page.png" alt="new image" /> \
						<img src="/Static/images/page.png" alt="new image" />'
					);
				}
				else if (page == 1) {
					$(rightpage).css("color", "red");
				}
				$(this).dialog( "close" ); 
			}
		}
	});
	
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
	
	//Save album
	/*
	$('#savealbum').on("click", function () {
		if($("#albumtitle").val().length == 0)
			alert("Please add a title to your album!");
		else
			window.location="../";
	});
	*/
});
	