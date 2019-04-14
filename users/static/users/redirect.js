var counter = 5;

var timer = setInterval(function() {
  counter--;
  document.querySelector("#countdown").innerHTML = counter;

  if (counter == 0)
  {
    clearInterval(timer);
    window.location = "/";
  }
}, 1000);
