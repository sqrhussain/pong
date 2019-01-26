function startRoute() {

  var vid = document.getElementById("StartSound");
  vid.play();

var input = document.getElementById("username");
var storedValue = localStorage.getItem("storage");
if(storedValue != null)
{
  input.setAttribute("placeholder", storedValue);
}

       document.getElementById("StartButton").onclick = function () {
       localStorage.setItem("storage", input.value);


            location.href = "#play";
        };
}
