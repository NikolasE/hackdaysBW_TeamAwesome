/*
function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}


// Stuff which runs after the js is fully loaded and ready
$(document).ready(function () {

  // initial connect to socket
  var socket = io.connect('http://localhost:8000/', { secure: true });


  // connect a button press event to the button2
  document.getElementById("start_programme").onclick = function () {
    console.log("Start Programme Button pressed");
    socket.emit('client_server_namespace', { 'page': 1, 'button': 1 });
    sleep(200);
    location.href = "/s";
  }

  

});
*/
window.addEventListener("load", function() {
    rotateDirection(0);
    window.scrollTo(0,document.body.scrollHeight);
  });


//Kompass
if (window.DeviceOrientationEvent) {
  // Listen for the deviceorientation event and handle the raw data
  window.addEventListener('deviceorientation', function(eventData) {
    var compassdir;

    if(event.webkitCompassHeading) {
      // Apple works only with this, alpha doesn't work
      compassdir = event.webkitCompassHeading;
    } else {
    compassdir = event.alpha;
    }
        rotateDirection(compassdir);
  });
}
function rotateDirection(deg) {
    var svg = document.getElementById('location');
    if (svg) {
        svg.setAttribute('transform','rotate('+deg+', 60, 850)');
        console.log("rotation");
    }else{
        console.log("noElement");
    }
}