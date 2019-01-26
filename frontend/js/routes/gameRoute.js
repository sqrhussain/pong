function gameRoute() {

    // init game view
    var gameController = new GameController();
    var vid = document.getElementById("StartSound");
    vid.pause();

    document.getElementById("EndButton").onclick = function () {
        location.href = "#lose";
    };
}
