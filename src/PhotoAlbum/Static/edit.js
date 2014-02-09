var page;		// 0 = leftpage, 1 = rightpage
var imageplace;	// current picture
var pagecount;  // how many pages we have added to the album (total - 2)
var layouts;	// layouts array
var images;
var jsonlayouts, jsonimages; // json variables to receive django data
var currentpage;	// current displayed page

$(document).ready(function() {
	//Initialize
	pagecount = currentpage = 0;
	layouts = new Array();
	layouts[0] = layouts[1] = 0;
	
	images = new Array();
	images[pagecount] = new Array();
	images[pagecount + 1] = new Array();
	
	initpage(0);
	initpage(1);
	
	//Setup dialog windows
	$("#selectlayout").dialog({
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
				var caption = $('input[name=piccaption]').val();
				if (url && caption) {
					uploadimage(url, caption);
					$(this).dialog( "close" ); 
				}
			}
		}
	});
	
	if (jsonlayouts)
		loadalbum();
	
	// display page count
	$("#pagecounter").html("<p>< " + (currentpage / 2 + 1) + " / " + (pagecount / 2 + 1) + " ></p>");
});

function initpage(index) {				// index 0 = left, 1 = right
	if (index == 0)	{
		$("#leftpage").html("");
		$("#leftpage").css("background-image", "url('/Static/images/layout.png')");
		$("#leftpage").css("cursor", "pointer");
		
		// Add layout to the left page
		$('#leftpage').on("click", function () {
			$('input[name=layoutselect]').removeAttr("checked");
			$('#selectlayout').dialog("open");
			page = 0;	
		});
	}
	else {
	// Add layout to the right page
		$("#rightpage").html("");
		$("#rightpage").css("background-image", "url('/Static/images/layout.png')");
		$("#rightpage").css("cursor", "pointer");
		
		$('#rightpage').on("click", function () {
			$('input[name=layoutselect]').removeAttr("checked");
			$('#selectlayout').dialog("open");
			page = 1;	
		});
	}
}

function applylayout(index) {			// index: selected layout index
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
	
	// Save layout
	// console.log("layouts");
	layouts[page + currentpage] = index;

	/*for (i = 0; i < layouts.length; ++i) {
		console.log(layouts[i]);
	}*/
	
	// Create click function for the images
	$(".imageholder").click(function (event) {
		imageplace = $(event.target).closest("div").attr("id");
		// get the last character of the id
		page = imageplace[imageplace.length - 1];
		
		$('input[name=picurl]').val('');	// clear textboxes
		$('input[name=piccaption]').val('');
		$('#uploadpic').dialog("open");		// pops up dialog to enter picture url
	});
}

function uploadimage (url, caption) {	// display picture: url and caption
	side = page == 0 ? "leftpage" : "rightpage";
	$("#" + side).find("#" + imageplace).html(
		'<figure> \
			<img alt="' + url + '" src="' + url + '" > \
			<figcaption>'+ caption +'</figcaption> \
		</figure>'
	);
	$("#" + side).find("#" + imageplace).css("background-image", "none");
}

function deletelayout(index) {			// index 0 = left, 1 = right
	side = index == 0 ? "leftpage" : "rightpage";
	
	if (confirm("Are you sure you want to delete the layout?")) {	
		$("#" + side).html("");
		$("#" + side).css("background-image", "url('/Static/images/layout.png')");
		$("#" + side).css("cursor", "pointer");
		
		initpage(index);
		
		// reset layouts array
		layouts[index + currentpage] = 0;
		images[index + currentpage] = new Array();
	}
}

function newpage() {	
	savepages();
	
	pagecount += 2;
	currentpage = pagecount;
	
	layouts[pagecount] = 0;
	layouts[pagecount + 1] = 0;
	
	images[pagecount] = new Array();
	images[pagecount + 1] = new Array();
	
	initpage(0);
	initpage(1);
	
	$("#leftmove").css("display", "block");
	
	$("#pagecounter").html("<p>< " + (currentpage / 2 + 1) + " / " + (pagecount / 2 + 1) + " ></p>");
}

function savepages() {			
	$("#leftpage div").each(function( index ) {
		//console.log( index + ": " + $(this).find("figcaption").html() );		
		if ($(this).find("img").attr("src") != null)
			images[currentpage][index] = {'src': $(this).find("img").attr("src"), 'caption': $(this).find("figcaption").html() };
		else
			images[currentpage][index] = {'src': "", 'caption': ""};
	});
	
	$("#rightpage div").each(function( index ) {
		//console.log( index + ": " + $(this).find("figcaption").html() );
		if ($(this).find("img").attr("src") != null)
			images[currentpage + 1][index] = {'src': $(this).find("img").attr("src"), 'caption': $(this).find("figcaption").html() };
		else
			images[currentpage + 1][index] = {'src': "", 'caption': ""};
	});
	
	console.log("save images");
	for (i = 0; i < images.length; ++i)
		for (j = 0; j < images[i].length; ++j) {
			console.log(images[i][j].src);
		}
}

function save_album() {
	// title validation
	
	if ($("#albumtitle").val() == "") {
		alert("Please add a title to your album!");
		return false;
	}
	else {	
		savepages();
		
		var jsonlayouts = JSON.stringify(layouts);
		$("#layouts").val(jsonlayouts);
		
		var jsonimages = JSON.stringify(images);
		$("#images").val(jsonimages);
		
		return true;
	}
}

function moveleft() {
	savepages();
	
	currentpage -= 2;
	
	console.log("currentpage: " + currentpage + ", " + "pagecount: " + pagecount);
	
	if (currentpage == 0) {
		$("#leftmove").css("display", "none");
	}
	
	$("#addpage").css("display", "none");
	$("#rightmove").css("display", "block");
	
	displaypages();
	
	$("#pagecounter").html("<p>< " + (currentpage / 2 + 1) + " / " + (pagecount / 2 + 1) + " ></p>");
}

function moveright() {
	savepages();
	
	currentpage += 2;
	
	console.log("currentpage: " + currentpage + ", " + "pagecount: " + pagecount);
	
	if (currentpage == pagecount) {
		$("#rightmove").css("display", "none");
		$("#addpage").css("display", "block");
	}
	
	$("#leftmove").css("display", "block");
	
	console.log("layouts");
	for (i = 0; i < layouts.length; ++i)
		console.log(layouts[i]);
	
	displaypages();
	
	$("#pagecounter").html("<p>< " + (currentpage / 2 + 1) + " / " + (pagecount / 2 + 1) + " ></p>");
}

function displaypages() {
	page = 0;							// 0 = leftpage
	
	if (layouts[currentpage] != 0)
		applylayout(layouts[currentpage]);
	else
		initpage(page);
		
	$("#leftpage div").each(function( index ) {
		//console.log( index + ": " + $(this).find("figcaption").html() );
		
		if (images[currentpage][index].src != '') {
			$(this).html(
				'<figure> \
					<img alt="' + images[currentpage][index].src + '" src="' + images[currentpage][index].src + '" > \
					<figcaption>'+ images[currentpage][index].caption +'</figcaption> \
				</figure>'
			)
			$(this).css("background-image", "none");
		}
	});
	
	page = 1;							// 1 = rightpage
	
	if (layouts[currentpage + 1] != 0)
		applylayout(layouts[currentpage + 1]);
	else
		initpage(page);
	
	$("#rightpage div").each(function( index ) {
		//console.log( index + ": " + $(this).find("figcaption").html() );
		if (images[currentpage + 1][index].src != '') {
			$(this).html(
				'<figure> \
					<img alt="' + images[currentpage + 1][index].src + '" src="' + images[currentpage + 1][index].src + '" > \
					<figcaption>'+ images[currentpage + 1][index].caption +'</figcaption> \
				</figure>'
			)
			$(this).css("background-image", "none");
		}
	});
}

function loadalbum() {
	var i = 0;
	for (var key in jsonlayouts) {
		layouts[i] = jsonlayouts[key];
		images[i] = new Array();
		++i;
	}
	
	pagecount = layouts.length - 2;
	if (pagecount > 1) {
		$("#addpage").css("display", "none");
			$("#rightmove").css("display", "block");
	}
	
	i = 0;
	var imgcount = 0;	// number of pictures on the page
	for (var key in jsonimages) {
		while (layouts[i] == 0)
			++i;
		
		images[i][imgcount] = {'src' : jsonimages[key].source, 'caption' : jsonimages[key].title}
		
		// layouts array contains the number of images of the page, except:
			// on layout 4 we have 3 image places
			// on layout 0 we have no images 
		if (imgcount == layouts[i] - 1 || layouts[i] == 0 || (layouts[i] == 4 && imgcount == 2)) {
			++i;			
			imgcount = 0;
		}
		else {	
			++imgcount;
		}
	}
	
	for (i = 0; i < layouts.length; ++i) {
			console.log(layouts[i]);
		}
	
	console.log("images");
	for (i = 0; i < images.length; ++i) {
		console.log(i)
		for (j = 0; j < images[i].length; ++j) {
			console.log(images[i][j].src);
		}
	}
		
	displaypages();
}
	