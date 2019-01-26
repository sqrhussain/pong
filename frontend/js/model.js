// listen to server, send messages to game view
function Model() {
  this.username = '';
  this.gameServer = null;
  this.view = null;
  this.own = 0; // just fix that the player is always #0 on their own device (the paddle to the left)
  this.opp = 1;
  this.playerMessage = {type:"playername", name: "???"};

  this.initWebsocket();
}

Model.prototype.initWebsocket = function() {
  this.gameServer = new WebSocket(config.gameServerUrl);

  var self = this;
  this.gameServer.onmessage = function(event) {

    //console.log("model recv: " + event.data);
    msg = JSON.parse(event.data);
    // processor
    switch(msg.type){
    case "handshake":
        this.send(this.playerMessage);
        break;
    case "ball":
    	self.view.updateBallPosition(msg.position, msg.velocity);
    	break;
    case "paddle":
    	self.view.updatePaddleY(msg.player,msg.y)
    	break;
    case "score":
      self.view.updateScore(msg.score);
      break;
    case "game_state":
      self.view.onGameEnd();
      break;
    case "hit":
      self.view.onHit(msg.hitObject)
      break;
    // TODO process rest of the messages...
    default:
    	break;
    }
  }
};

Model.prototype.setView = function(view) {
	this.view = view;
}

Model.prototype.send = function(message) {
	console.log("model send: " + JSON.stringify(message))
  	this.gameServer.send(JSON.stringify(message));
};

Model.prototype.down = function() {
	this.send({type:"move",direction:"down"});
}

Model.prototype.up = function() {
	this.send({type:"move",direction:"up"});
}

Model.prototype.playername = function(name) {
    this.playerMessage = {type:"playername", name: name};
}
