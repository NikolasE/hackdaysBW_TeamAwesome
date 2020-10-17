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
  /*
  // connect a button press event to the button2
  document.getElementById("dropdownMenu").onclick = function (event) {
    var element = document.getElementById("dropdownMenu");
    for (var i = 0; i < element.children.length; i++) {
      console.log(element.children.length);

      (function (index) {

        element.children[i].onclick = function () {
          console.log('thetext');
          var thetext = element.getElementsByTagName('a')[index].innerHTML;
          console.log(thetext);
          // var thehref = element.getElementsByTagName('a')[index].href; get the href here once you hosted, for testing I will use the name
          var buttonelement = document.getElementById("dropdownMenuButton");
          buttonelement.innerText = thetext;

        }

      })(i);
    }
    console.log("drop Programme Button pressed");
    socket.emit('client_server_namespace', { 'page': '1', 'button': '2' });

  }
  */
  //Nav bar buttons:
  document.getElementById("nav_page1").onclick = function () {
    console.log("Navbar to page1");
    socket.emit('client_server_namespace', { 'page': 1, 'button': 1 });
    sleep(200);
    location.href = "/";
  }
  document.getElementById("nav_page2").onclick = function () {
    console.log("Navbar to page2");
    socket.emit('client_server_namespace', { 'page': 1, 'button': 1 });
    sleep(200);
    location.href = "/s";
  }
  document.getElementById("nav_page3").onclick = function () {
    console.log("Navbar to page3");
    socket.emit('client_server_namespace', { 'page': 1, 'button': 1 });
    sleep(200);
    location.href = "/s";
  }
  document.getElementById("nav_page4").onclick = function () {
    console.log("Navbar to page4");
    socket.emit('client_server_namespace', { 'page': 1, 'button': 1 });
    sleep(200);
    location.href = "/s";
  }
  document.getElementById("nav_page5").onclick = function () {
    console.log("Navbar to page6");
    socket.emit('client_server_namespace', { 'page': 1, 'button': 1 });
    sleep(200);
    location.href = "/l";
  }
  document.getElementById("nav_page6").onclick = function () {
    console.log("Navbar to page6");
    socket.emit('client_server_namespace', { 'page': 1, 'button': 1 });
    sleep(200);
    location.href = "/v";
  }

});
