function GameView(model) {

  this.size = {w: 1080,h: 720};
  this.padding = {w: 5, h: 5};


  this.paddleSize = {w: 20,h: 160};
  this.ballRadius = 20;


  this.model = model;

  this.paddleX = [this.padding.w,this.size.w - this.padding.w - this.paddleSize.w];

  // to be controlled by model
  this.paddle = [{x:this.paddleX[0],
                  y: this.size['h'] / 2 - this.paddleSize['h'] / 2},
                 {x:this.paddleX[1],
                  y: this.size['h'] / 2 - this.paddleSize['h'] / 2}
                ];
  this.ballPosition = {x: this.size.w / 2, y: this.size.h / 2};
  this.ballPositionServer = {x: this.size.w / 2, y: this.size.h / 2};
  this.ballVelocityServer = {x: 0, y: 0};
  this.score = [0,0];
  this.player = ["Player 1", "Player 2"];

  this.canvas = document.getElementById('game-canvas').getContext('2d');
  document.getElementById('game-canvas')
      .setAttribute('width', this.size.w);
  document.getElementById('game-canvas')
      .setAttribute('height', this.size.h);


  this.fps = 15;
  this.now;
  this.then = Date.now();
  this.interval = 1000 / this.fps;
  this.delta;

  this.messageText = "";

  var self = this;
  requestAnimationFrame(function () {
    self.gameLoop();
  });

}

GameView.prototype.cleanCanvas = function() {
  this.canvas.fillStyle = 'red'; // TEMPORARILY: just to see the borders
  this.canvas.fillRect(0, 0, this.size.w, this.size.h);
};


GameView.prototype.updateBallPosition = function(position, velocity) {
  this.ballPositionServer = position;
  this.ballVelocityServer = velocity;
  this.ballPosition = position;
};

// assume paddle position refers to the top left corner of the paddle
GameView.prototype.updatePaddleY = function(player,y) {
  this.paddle[player]['y'] = y;
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
  // may also have two other divs in which we plot scores
  //score 1
  this.canvas.textAlign = "end";
  this.canvas.fillText(this.score[0], 520, 50);
  //score 2
  this.canvas.textAlign = "start";
  this.canvas.fillText(this.score[1], 560, 50);
  this.canvas.font = "70px Arcade Classic";

};
GameView.prototype.drawPlayer = function(){
  this.canvas.font = "50px Arcade Classic";
  //player 1
    this.canvas.textAlign = "end";
    this.canvas.fillText(this.player[0], 400, 50);
      //player 2
    this.canvas.textAlign = "start";
    this.canvas.fillText(this.player[1], 680, 50);
};

GameView.prototype.drawLine = function(){
  this.canvas.moveTo(540, 0);
  this.canvas.lineTo(540, 720);
  this.canvas.stroke();
};

GameView.prototype.drawMessageText = function(){
  this.canvas.font = "60px Arcade Classic";
  this.canvas.textAlign = "center";
  this.canvas.fillText(this.messageText, this.size.w/2, this.size.h/2 + 100);
};

GameView.prototype.onHit = function(hitObject){
  // TODO make noise according to the hit object ("wall"/"paddle"/"out");
  if(hitObject == "wall")
    this.ballHitWall();
  else if(hitObject == "paddle")
    this.ballHitPaddle();
  else if(hitObject == "out")
    this.ballHitGoal();
};

GameView.prototype.update = function(delta) {
  this.ballPosition.x = this.ballPositionServer.x + (this.ballVelocityServer.x * delta / 1000);
  this.ballPosition.y = this.ballPositionServer.y + (this.ballVelocityServer.y * delta / 1000);
};

GameView.prototype.draw = function(delta) {
  this.cleanCanvas();
  this.drawBall(this.ballPosition);
  this.drawPaddle(this.paddle[0]);
  this.drawPaddle(this.paddle[1]);
  this.drawScore();
  this.drawPlayer();
  this.drawLine();
  this.drawMessageText();
};

GameView.prototype.gameLoop = function() {
  var self = this;
  requestAnimationFrame(function () {
    self.gameLoop();
  });

  this.now = Date.now();
  this.delta = this.now - this.then;

  if (this.delta > this.interval) {
    this.then = this.now - (this.delta % this.interval);
    this.update(this.delta);
    this.draw(this.delta);
  }
};

GameView.prototype.ballHitWall = function() {
  var vid = document.getElementById("WallSound");
  vid.play();

};

GameView.prototype.ballHitPaddle = function() {
  var vid = document.getElementById("PaddleSound");
  vid.play();

};

GameView.prototype.ballHitGoal = function(){
  // todo ... could play a sound!
};

GameView.prototype.onGameEnd = function(){
  // currently nothing to do here
};

GameView.prototype.onWaiting = function(){
  this.messageText = "Waiting for the other player"
};

GameView.prototype.onPlaying = function(){
  this.messageText = ""
};

