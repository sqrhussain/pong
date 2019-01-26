function gameWinRoute() {
    var vid = document.getElementById("VictorySound");
    vid.play();

    var highScoreButton = document.getElementById("HighScoreButton1");
    if (highScoreButton) {
        highScoreButton.onclick = function () {
            location.href = "#highscore";
        };
    }

    document.getElementById("StartEndButton1").onclick = function () {
        location.href = "#";
    };

    document.getElementById("DocumentButton1").onclick = function () {
        location.href = "documentation.html";
    };
}
