// listen for inputs from view and send to model
function GameController(){

var name = localStorage.getItem("storage");
model.playername(name);
  var model = new Model();
  var gameView = new GameView(model);
  model.setView(gameView);

  var self = this;
  this.onKeydown = function handleKey(event){
    if(event.keyCode == 38){ // up
      model.up();
    } else if(event.keyCode == 40){// down
      model.down();
    }
    //  else if(event.keyCode == 27){
    // 	self.destroy();
    // }
  }
  // handling user input
  document.addEventListener("keydown",this.onKeydown);

}

GameController.prototype.destroy = function(){
	document.removeEventListener("keydown",this.onKeydown);
}