
### Messaging protocol

#### Server to client

1. Ball position {type:"ball", position:{x,y}}

2. Paddle position {type:"paddle", player:(0/1), y}

3. Score {type:"score", score:[s0,s1]}

4. Game start {type:"gameStart", countdown:(3/2/1/0)}

5. Hit {type:"hit", hitObject:("wall"/"paddle")}

