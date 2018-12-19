function Model() {
  this.username = '';
  this.gameServer = null;
  this.view = null;

  this.initWebsocket();
}

Model.prototype.initWebsocket = function() {
  this.gameServer = new WebSocket(config.gameServerUrl);

  var self = this;
  this.gameServer.onmessage = function(event) {
    console.log("recv: " + event.data);
    msg = JSON.parse(event.data);
    // processor
    switch(msg.type){
    case "ball":
    	self.view.updateBallPosition(msg.position);
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
