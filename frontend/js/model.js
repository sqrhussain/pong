function Model() {
  this.username = '';
  this.gameServer = null;

  this.initWebsocket();
}

Model.prototype.initWebsocket = function() {
  this.gameServer = new WebSocket(config.gameServerUrl);

  this.gameServer.onmessage = function(event) {
    msg = event.data;
    console.log("recv: " + msg)
    // processor
    switch(msg.type){
    case "ball":
    	this.view.updateBallPosition(msg.position)
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
	console.log("send: " + msg)
  	this.gameServer.send(message);
};

Model.prototype.down = function() {
	this.send({type:"move",direction:"down"});
}

Model.prototype.up = function() {
	this.send({type:"move",direction:"up"});
}
