function GameView(model) {

  this.size = {w:300,h:150};
  this.padding = {w:5, h:5};


  this.paddleSize = {w:10,h:40};
  this.ballRadius = 5;

  this.model = model;

  this.ownPaddleX = this.padding.w;
  this.opponentPaddleX = this.size.w - this.padding.w - this.paddleSize.w;

  // should be controlled by model
  this.ownPaddlePosition = {x:this.ownPaddleX, y:75};
  this.opponentPaddlePosition = {x:this.opponentPaddleX, y:25};
  this.ballPosition = {x: 200, y: 60};

  this.canvas = document.getElementById('game-canvas').getContext('2d');

  var self = this;
  requestAnimationFrame(function () {
    self.gameLoop();
  });
}

GameView.prototype.cleanCanvas = function() {
  this.canvas.fillStyle = 'grey'; // TEMPORARILY: just to see the borders
  this.canvas.fillRect(0, 0, this.size.w, this.size.h);
};


GameView.prototype.updateBallPosition = function(position) {
  this.ballPosition = position;
};

// assume paddle position refers to the top left corner of the paddle
GameView.prototype.updateOwnPaddleY = function(y) {
  this.ownPaddlePosition.y = y;
};
GameView.prototype.updateOpponentPaddleY = function(y) {
  this.opponentPaddlePosition.y = y;
};

GameView.prototype.drawBall = function(position) {
  this.canvas.beginPath();
  this.canvas.arc(position.x, position.y, this.ballRadius, 0, 2 * Math.PI, false);
  this.canvas.fillStyle = 'white';
  this.canvas.fill();
  this.canvas.lineWidth = 5;
  this.canvas.strokeStyle = '#ffffff';
  this.canvas.stroke();
};

GameView.prototype.drawPaddle = function(position) {
  this.canvas.fillStyle = 'white';
  this.canvas.fillRect(position.x, position.y, this.paddleSize.w, this.paddleSize.h);
};


GameView.prototype.draw = function() {
  this.cleanCanvas();
  this.drawBall(this.ballPosition);
  this.drawPaddle(this.ownPaddlePosition);
  this.drawPaddle(this.opponentPaddlePosition);
};

GameView.prototype.gameLoop = function() {
  this.draw();
};
