gcc -c ai_server.c -o ai_server.o
gcc ai_server.o othello.o arbre.o -o Egaroucid/bin/exec
cd Egaroucid/bin/
./exec