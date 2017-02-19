document.addEventListener('scroll', function(){
  var anchors = document.getElementsByTagName("a");
  for (var i = 0; i < anchors.length; i++){
    anchors[i].addEventListener("focus", myFunction);
  }
}, false);

function myFunction(e){
  console.log("a");
  var imgSrcVal = $(e.target).find("img").attr("src");

  if(imgSrcVal != undefined) {
    httpPOST(imgSrcVal);
  }
}


function httpPOST(data){       
  var http = new XMLHttpRequest();
  var url = "https://kzpree.me:5000/getDescription";
  var params = "data="+data;
  http.open("POST", url, true);

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


