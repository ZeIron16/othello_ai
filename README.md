# Othello_ai
## STILL IN PROGRESS (This is only the app's background)

This code is playable and use Egaroucid AI is the most difficult level.

You can choose the colour of the bot and the difficulty level.

This is a **Linux** version, to use it, at least use a WSL.

This was also not created to play alone but is supposed to use communication with a gui server. 
You can use it but in difficulty 3, an other terminal is opened with egaroucid, even if you can ignore it, don't close it until you finish your game.

## What is implemented :

  -> The game itself playable in the shell

  -> Theorical openings System
  
  -> MinMax alpha-beta with a complex heuristic

  -> An adaptation od Egaroucid
  
# How to use this programm:

## Dowload Everything:
-> You need to download all the files

-> The Egaroucid dir is an adaptation of the open source Othello bot by Nyanyan: https://github.com/Nyanyan/Egaroucid

-> Use chmod 777 on both script.sh and start.sh (in Egaroucid/bin)

-> Then, go to Egaroucid/bin/ in you terminal and execute:

	clang++ -O2 ../src/Egaroucid_for_Console.cpp -o ../bin/Egaroucid_for_Console.out -mtune=native -march=native -pthread -std=c++20 -DHAS_ARM_PROCESSOR

## Lauch the programm:
-> To execute the code, simply execute script.sh

-> Then you can choose the colour of the bot

-> Here are the different difficulty levels:

	1: Naive heuristic

	2: Complex heuristic

	3: Egaroucid -> ATTENTION: Make sure to wait that Egaroucid has started in the new terminal before playing


## Appendix:

I apologize for the few french words that are currently prensent in some file names (it will be corrected next update).

If you also find any bug, please contact me.
