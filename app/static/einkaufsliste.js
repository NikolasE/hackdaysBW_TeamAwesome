function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}
function gotonavigator() {
  console.log("Go To Navigator");
  document.getElementById("overlay").style.display = "block";
  location.href = "/navigation";
}
function in_my_basket(id) {
  console.log(document.getElementById(id).style.background)
  if (document.getElementById(id).style.background == "#ffe10050") {

    document.getElementById(id).style.background = "#dee2e6";

  } else {
    document.getElementById(id).style.background = "#ffe10050";
  }

}

// Stuff which runs after the js is fully loaded and ready
$(document).ready(function () {

  // initial connect to socket
  var socket = io.connect('http://localhost:8000/', { secure: true });

  document.getElementById("overlay").style.display = "none";




  // connect a button press event to the button2
  document.getElementById("start_programme").onclick = function () {
    console.log("Start Programme Button pressed");
    socket.emit('client_server_namespace', { 'page': 1, 'button': 1 });
    sleep(200);
    location.href = "/s";
  }


});
