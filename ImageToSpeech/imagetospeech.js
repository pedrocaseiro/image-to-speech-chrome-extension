var msg = new SpeechSynthesisUtterance('Hello World');

//var imgs = document.getElementsByTagName("img");
var anchors = document.getElementsByTagName("a");
var images = [];
var imagesDescription = {};

for (var i = 0; i < anchors.length; ++i){
  console.log(i);
  anchors[i].addEventListener("focus", myFunction);
  }



//chrome.contextMenus.create({
//title: "Search: %s", 
//contexts:["page", "selection"], 
//onclick: clickHandler,
//});
function myFunction(e){

  var imgSrcVal = $(anchors[i]).find("img").attr("src");
  if(imgSrcVal != undefined) {
    // POST AO SERVER
    window.speechSynthesis.speak(msg);
  }
}

