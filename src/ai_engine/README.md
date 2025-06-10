# How to use this programm:

## Dowload Everything:
-> You need to download all the files

-> The Egaroucid dir is an adaptation of the open source Othello bot by Nyanyan: https://github.com/Nyanyan/Egaroucid

-> Use chmod 777 on both script.sh and start.sh (in Egaroucid/bin)

-> Then, go to Egaroucid/bin/ in you terminal and execute:

	clang++ -O2 ../src/Egaroucid_for_Console.cpp -o ../bin/Egaroucid_for_Console.out -mtune=native -march=native -pthread -std=c++20 -DHAS_ARM_PROCESSOR

## Lauch the programm:

### Work-Alone version:

-> To execute the code, simply execute script.sh

-> Then you can choose the colour of the bot

-> Here are the different difficulty levels:

	1: Naive heuristic

	2: Complex heuristic

	3: Egaroucid -> ATTENTION: Make sure to wait that Egaroucid has started in the new terminal before playing

### Competitive version:

-> If you want to execute it in server mode from here, in script.sh, modify main.c by ai_server.c

## Appendix:

I also apologize for the few french words that are currently prensent in some file names.

arbre = tree

ouverture = opening
