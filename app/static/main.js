// Stuff which runs after the js is fully loaded and ready

/*
$(document).ready(function() {

    // initial connect to socket
    var socket = io.connect('https://localhost:8000/', {secure: true});
    console.log("[+] Connected");

    // connect a button press event to the button1
    document.getElementById("button1").onclick = function() {
        console.log("Button1 pressed");

        // Emit a message to the 'client_server_namespace'
        socket.emit('client_server_namespace', {'button':'1'});
    }

    // connect a button press event to the button2
    document.getElementById("button2").onclick = function() {
        console.log("Button2 pressed");

        socket.emit('client_server_namespace', {'button':'2'});
    }

    // connect a button press event to the button3
    document.getElementById("button3").onclick = function() {
        console.log("Button3 pressed");

        socket.emit('client_server_namespace', {'button':'3'});
    }

    // Message recieved from server in the 'server_client_namespace
    // You can have as many namespaces as you whish... 
    socket.on("server_client_namespace", function(message) {
    	console.log( message);
	document.getElementById("value").innerHTML = message.button;
    });
});
*/

//Kompass
if (window.DeviceOrientationEvent) {
  // Listen for the deviceorientation event and handle the raw data
  window.addEventListener('deviceorientation', function(eventData) {
    var compassdir;

    if(event.webkitCompassHeading) {
      // Apple works only with this, alpha doesn't work
      compassdir = event.webkitCompassHeading;
    }
    else compassdir = event.alpha;

    document.getElementById("direction").innerHTML = Math.ceil(compassdir);

  });
}

//rotate
function rotateDirection(idStr, deg) {
    var domElemnt = document.getElementById("location");
    if (domElemnt) {
        domElemnt.style.transform = "rotate(50deg)";
        console.log("rotation")
    }
}
rotateDirection("location", 5);
