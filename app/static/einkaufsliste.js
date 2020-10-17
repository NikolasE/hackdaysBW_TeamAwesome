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
  console.log(id);
  val = document.getElementById("overlay").style.background;
  console.log(val);


  if (document.getElementById(id).style.background == "rgba(255, 225, 0, 0.314) none repeat scroll 0% 0%") {
    document.getElementById(id).style.background = "#dee2e6";
    socket.emit('client_server_namespace', { 'product': id, 'inbasket': 0 });
  } else {
    document.getElementById(id).style.background = "#ffe10050";
    socket.emit('client_server_namespace', { 'product': id, 'inbasket': 1 });

  }

}

// Stuff which runs after the js is fully loaded and ready
$(document).ready(function () {

  // initial connect to socket
  var socket = io.connect('http://localhost:8000/', { secure: true });

  document.getElementById("overlay").style.display = "none";

});
