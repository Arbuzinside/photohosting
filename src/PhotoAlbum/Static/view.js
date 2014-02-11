var page;		// 0 = leftpage, 1 = rightpage
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
	
	loadalbum();
	
	// display page count
	$("#pagecounter").html("<p>< " + (currentpage / 2 + 1) + " / " + (pagecount / 2 + 1) + " ></p>");
});

function moveleft() {
	currentpage -= 2;
	
	if (currentpage == 0) {
		$("#leftmove").css("display", "none");
	}
	
	$("#rightmove").css("display", "block");
	
	displaypages();
	
	$("#pagecounter").html("<p>< " + (currentpage / 2 + 1) + " / " + (pagecount / 2 + 1) + " ></p>");
}

function moveright() {	
	currentpage += 2;
	
	if (currentpage == pagecount) {
		$("#rightmove").css("display", "none");
	}
	
	$("#leftmove").css("display", "block");
	
	displaypages();
	
	$("#pagecounter").html("<p>< " + (currentpage / 2 + 1) + " / " + (pagecount / 2 + 1) + " ></p>");
}

function applylayout(index) {			// index: selected layout index
	var pagetoload = page == 0 ? "leftpage" : "rightpage";
	$("#" + pagetoload).off();
	
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
}

function displaypages() {	
	if (layouts[currentpage] != 0) {
		page = 0;
		applylayout(layouts[currentpage]);
	}
		
	$("#leftpage div").each(function( index ) {
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
	
	if (layouts[currentpage + 1] != 0) {
		page = 1;
		applylayout(layouts[currentpage + 1]);
	}
	
	$("#rightpage div").each(function( index ) {
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
	if (pagecount > 1)
		$("#rightmove").css("display", "block");
	
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

(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/all.js#xfbml=1";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));