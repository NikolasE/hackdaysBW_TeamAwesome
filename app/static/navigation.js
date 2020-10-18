// initial connect to socket
var socket = io.connect('https://localhost:8000/', { secure: true });
 console.log("[+] Connected");

window.addEventListener("load", function() {
    document.getElementById("overlay").style.display = "none";
    rotateDirection(0);
    window.scrollTo(0,document.body.scrollHeight);
  });

//Kompass
function startCompass() {
  if (isIOS) {
    DeviceOrientationEvent.requestPermission()
      .then((response) => {
        if (response === "granted") {
          window.addEventListener("deviceorientation", handler, true);
        } else {
          alert("has to be allowed!");
        }
      })
      .catch(() => alert("not supported"));
  } else {
    window.addEventListener("deviceorientationabsolute", handler, true);
  }
}


if (window.DeviceOrientationEvent) {
  // Listen for the deviceorientation event and handle the raw data
  window.addEventListener('deviceorientation', function(eventData) {
    var compassdir;
    compassdir = 0;
    if(event.webkitCompassHeading) {
        // Apple works only with this, alpha doesn't work
        compassdir = event.webkitCompassHeading;
    } else {
        compassdir = event.alpha;
    }
        rotateDirection(compassdir);
  }, true);
}

function rotateDirection(deg) {
    var svg = document.getElementById('location');
    if (svg) {
        svg.setAttribute('transform','rotate('+ deg +', '+ document.getElementById("user_x").innerHTML +', '+ document.getElementById("user_y").innerHTML +')');
        console.log("rotation");
    }else{
        console.log("noElement");
    }
}

function gotonavigator(redirect) {
  console.log("Go To Navigator");
  document.getElementById("overlay").style.display = "block";
  location.href = redirect;
}
