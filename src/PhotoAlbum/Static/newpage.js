$(document).ready(function() {

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
						'<img src="/Static/images/page.png" width="40" height="60" alt="new image" /> \
						<img src="/Static/images/page.png" width="40" height="60" alt="new image" />'
					);
				}
				else if (page == 1) {
					$(rightpage).css("color", "red");
				}
				$(this).dialog( "close" ); 
			}
		}
	});
			
	$('#leftpage').on("click", function () {
        $('#dialog').dialog("open");
		page = 0;	
    });
	
	$('#rightpage').on("click", function () {
        $('#dialog').dialog("open");
		page = 1;	
    });
});
	