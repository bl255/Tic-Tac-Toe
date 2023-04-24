# Tic-Tac-Toe

### Introduction
Tic-tac-toe game with GUI, modes for one or two players, game sounds and option to change the game theme. The project was created as an assignment for the [Engeto](https://engeto.cz/) Python Academy. The original task was to create a terminal-based game. I added GUI based on Tkinter library to learn concepts of graphical user interference and object-oriented programming.

### Functionality
The game is played by clicking on the grid cells. Additional functions and settings are controlled by four buttons:

* Reset - resets the game
* Multiplayer - switches modes for one and two players
* Sounds - turns game sounds on and off
* Images - switches between vector and images theme

Algorithm for single player mode is based on [wikipedia description](https://en.wikipedia.org/wiki/Tic-tac-toe#Strategy) of Newell & Simon's 1972 program. The game plays either random choice or effective move at 4:6 rate. 

<img src=doc_images/image1.png width="400"><img src=doc_images/image2.png width="400">

### Structure
<img src=doc_images/scheme.png width="600">

### Final Thoughts
My aim was to separate functional a visual part of the game, so a new theme can be created and implemented.