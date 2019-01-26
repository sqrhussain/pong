function gameLoseRoute() {
    var vid = document.getElementById("LooseSound");
    vid.play();

    var highScoreButton = document.getElementById("HighScoreButton2");
    if (highScoreButton) {
        highScoreButton.onclick = function () {
            location.href = "#highscore";
        };
    }

    document.getElementById("StartEndButton2").onclick = function () {
        location.href = "#";
    };

    document.getElementById("DocumentButton2").onclick = function () {
        location.href = "documentation.html";
    };
}
