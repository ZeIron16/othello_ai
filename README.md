# Project S6 Group 11B: OthelloMora

This is the S6 project from EURECOM: an Othello game in the theme of Harry Potter.

## Abstract

The project aims to develop a full game of Othello / Reversi that include different features: an original design, an AI to play against, a voice detection to be able to while just speaking, and the possibility to play 
with other teams with different devices. It is powered by 3 Raspberry Pi (one for AI, one for speech detection, and one for UI and communication) and includes a microphone. The final product is a functional prototype of this system.

## Requirement
To successfully complete this project, we must meet several key requirements (features
presented in the abstract).

The first is the design, which has to be as original as possible: the goal here is to
differentiate teams on a creative criterion.

The second is to put in place a complete game system, letting players be able to play
locally. Additionally, it must include voice detection functionality, allowing players to
play without using a mouse or keyboard.

The third is to add an AI. This AI must be as efficient as possible: a competition
between the different teams’ AI is put in place at the end of the project. In addition,
local players also have to be able to play against the AI.

The last is to decide and implement the communication protocol between the different
teams (making us able to participate during the competition).


## Launch the Game

-> Clone the git

-> The UI of this project requier for now pygame and pygame_menu

-> The Audio also requier whisper_api

-> To play with the Audio against AI, you have to setup 2 servers:

    - the AI one:

        Go to ./src/ai_engine and follow the instructions

    - the Audio one:

        Execute  ./src/audio_control/whisper_api.py

-> To start the UI, go to ./src/main_raspberry and execute main.py

## How does it works:

When in the UI, you will have different options:

- Player 1 and 2 (1 is Black, 2 is White):
    
   - Computer is th AI
   - Human is mouse controlled
   - Online is server if Black, client if White

- Audio:
    - Off: human player is mouse controlled
    - On: human player is controlled with voice (ex: say C4)

- Language:
    - Choice between English (default), French or Chinese

- Theme:
    - Classic theme is classic version of othello (white and black pieces and ~green background)
    - Harry Potter theme is design to make you choose your house (with origianl pieces design for each house) 

- Server IP:
    - If you are online, this option appears
    - If server, choose the adress one which one you are hosting
    - If client, choose the one of the server you want to join
