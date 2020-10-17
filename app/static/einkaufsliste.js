var socket = io.connect('https://localhost:8000/', { secure: true });

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
  val = document.getElementById(id).style.background;
  console.log(val);


  if (document.getElementById(id+"_selected").innerHTML == "true") {
    element = document.getElementById(id+"_selected")
    element.parentElement.classList.remove("bg-warning");
    element.parentElement.classList.add("swatch-400");
    element.innerHTML = "false";
    socket.emit('client_server_namespace', { 'product': id, 'inbasket': 0 });

  } else {
    element = document.getElementById(id+"_selected")
    element.parentElement.classList.remove("swatch-400");
    element.parentElement.classList.add("bg-warning");
    element.innerHTML = "true";
    socket.emit('client_server_namespace', { 'product': id, 'inbasket': 1 });

  }

}

// Stuff which runs after the js is fully loaded and ready
$(document).ready(function () {

  // initial connect to socket


  document.getElementById("overlay").style.display = "none";

});
