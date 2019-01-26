function gameEndRoute() {

  /*var vid = document.getElementById("VictorySound");
  vid.play();*/
    var vid = document.getElementById("LooseSound");
  vid.play();

         document.getElementById("HighScoreButton").onclick = function () {
       location.href = "#highscore";
        };

               document.getElementById("StartEndButton").onclick = function () {
       location.href = "#";
        };

                       document.getElementById("DocumentButton").onclick = function () {
       location.href = "documentation.html";
        };

}
