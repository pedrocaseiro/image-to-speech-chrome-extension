
var anchors = document.getElementsByTagName("a");

for (var i = 0; i < anchors.length; i++){
  console.log(i);
  anchors[i].addEventListener("focus", myFunction);
  }



//chrome.contextMenus.create({
//title: "Search: %s", 
//contexts:["page", "selection"], 
//onclick: clickHandler,
//});
function myFunction(e){
	console.log("entrou");
	var imgSrcVal = $(e.target).find("img").attr("src");

	if(imgSrcVal != undefined) {
		
		console.log("ddd");
		// POST AO SERVER
		httpPOST(imgSrcVal);
		//window.speechSynthesis.speak(msg);

	}
}


function httpPOST(data){       
	var http = new XMLHttpRequest();
	console.log(data);
	var url = "https://0.0.0.0:5000/getDescription";
	var params = "data="+data;
	http.open("POST", url, true);

	//Send the proper header information along with the request
	//http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

	http.onreadystatechange = function() {//Call a function when the state changes.
		console.log(http.status);
	    if(http.readyState == 4 && http.status == 200) {
	    	var r = JSON.parse(http.responseText);
	        console.log(r["success"]);
	        window.speechSynthesis.speak(new SpeechSynthesisUtterance(r["success"]));
	    }
	}
	http.send(params);

}


