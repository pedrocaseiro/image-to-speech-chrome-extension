var msg = new SpeechSynthesisUtterance('Hello World');

var imgs = document.getElementsByTagName("img");
var imgSrcs = [];

console.log(imgs);
for (var i = 0; i < imgs.length; i++) {
  var b = 0;
  console.log("123");
  imgSrcs.push(imgs[i].src);
  console.log(imgs[i].src);
  window.speechSynthesis.speak(msg);
}

//chrome.contextMenus.create({
  //title: "Search: %s", 
  //contexts:["page", "selection"], 
  //onclick: clickHandler,
//});

