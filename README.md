Level_4_Arcade-Games
====================


""" Game Programming: Assignment 4 
Maze Game

Julian Morris and Jacob Riedel 11/3/14

Code: For part 3 on improving the game section, we decided to implement the smooth move and smooth falling. We did this by making the player move multiple steps for every tile it moves, just as you suggested. However, since Python is slow, it crashes fairly often if the global variable "steps" is set to anything above 4, where it only starts to get smooth when steps is more than 12, preferably 24. Also, the steps variable must be such that 24 is a multiple of steps. ex. 24/steps must be an integer so that the image doesn't get stuck between tiles.

To see our smooth implementation, set the steps global variable equal to 24. It does crash after around 15 seconds though, so beware.

Overall, the project was enjoyable, and a little bit on the easy side.
