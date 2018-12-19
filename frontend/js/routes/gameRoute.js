function gameRoute() {

  // init game view
  var model = new Model();
  var gameView = new GameView(model);
  model.setView(gameView);


  // todo: listen to server, send messages to game view

  // todo: listen for inputs from view and send to server

}
