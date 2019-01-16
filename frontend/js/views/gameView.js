function GameView(model) {

  this.size = {w:300,h:150};
  this.padding = {w:5, h:5};


  this.paddleSize = {w:10,h:40};
  this.ballRadius = 5;


  this.model = model;

  this.paddleX = [this.padding.w,this.size.w - this.padding.w - this.paddleSize.w];

  // to be controlled by model
  this.paddle = [{x:this.paddleX[0],
                  y:25/*dummy val*/},
                 {x:this.paddleX[1],
                  y:75/*dummy val*/}
                ];
  this.ballPosition = {x: 200, y: 60};
  this.score = [0,0];

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
GameView.prototype.updatePaddleY = function(player,y) {
  this.paddle[player] = y;
};

GameView.prototype.updateScore = function(scorePair) {
  this.score = scorePair;
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

GameView.prototype.drawScore = function(){
  // TODO plot score on canvas. Change canvas size and boundaries before.
  // may also have two other divs in which we plot scores
};

GameView.prototype.onHit = function(hitObject){
  // TODO make noise according to the hit object ("wall"/"paddle");

};


GameView.prototype.draw = function() {
  this.cleanCanvas();
  this.drawBall(this.ballPosition);
  this.drawPaddle(this.paddle[0]);
  this.drawPaddle(this.paddle[1]);
  this.drawScore();
};

GameView.prototype.gameLoop = function() {
  this.draw();

  var self = this;
  requestAnimationFrame(function () {
    self.gameLoop();
  });
};

GameView.prototype.ballHitWall = function() {

  var vid = document.getElementById("WallSound");
  vid.play();

};

GameView.prototype.ballHitPaddle = function() {

  var vid = document.getElementById("PaddleSound");
  vid.play();

};