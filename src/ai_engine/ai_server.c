#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include "othello.h"

#define PORT 12345
#define BUFFER_SIZE 4096

void get_move(const char *packet);

void handle_ai_command(const char* recv_buf, char* send_buf);

bool opening = true;

int move_played = 0;

Colour bot_colour = Empty;
Colour cur_colour = Black;

void initial(State* state)
{   
    move_played = 0;
    state->player = Black;
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            state->board[i][j] = Empty;

    state->board[N / 2 - 1][N / 2 - 1] = White;
    state->board[N / 2][N / 2] = White;
    state->board[N / 2 - 1][N / 2] = Black;
    state->board[N / 2][N / 2 - 1] = Black;
}

bool has_valid_move(State* state){
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (is_move_valid(state, i, j)) {
                return true;
            }
        }
    }
    return false;
}

State play(State state, int x, int y)
{

    if (state.board[x][y] != Empty)
    {
        return state;
    }

    int directions[8][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}, {-1, -1}, {-1, 1}, {1, -1}, {1, 1}};
    Colour oponent = (state.player == Black) ? White : Black;
    bool valid_move = is_move_valid(&state, x, y);
    if (valid_move)
    {
        state.board[x][y] = state.player;

        for (int d = 0; d < 8; d++)
        {
            int dx = directions[d][0], dy = directions[d][1];
            int i = x + dx, j = y + dy;
            bool oponent_crossed = false;

            while (i >= 0 && i < N && j >= 0 && j < N)
            {
                if (state.board[i][j] == Empty)
                {
                    break;
                }
                if (state.board[i][j] == oponent)
                {
                    oponent_crossed = true;
                }
                else if (state.board[i][j] == state.player)
                {
                    if (oponent_crossed)
                    {
                        int ii = x + dx, jj = y + dy;
                        while (ii != i || jj != j)
                        {
                            state.board[ii][jj] = state.player;
                            ii += dx;
                            jj += dy;
                        }
                        valid_move = true;
                    }
                    break;
                }
                i += dx;
                j += dy;
            }
        }
        state.player = (state.player == Black) ? White : Black;
        if (state.player == Black)
        {
            cur_colour = White;
        }
        else{cur_colour = Black;}
        return state;
    }

    if (!valid_move)
    {
        state.board[x][y] = Empty;
        if (state.player == Black)
        {
            cur_colour = White;
        }
        else{cur_colour = Black;}
        return state;
    }
}

//-----------------------------------------------------------------------------------------------------------------

TreeNode* play_opening(State* state, TreeNode* t)
{
    if (opening && t->num_children > 0)
    {

        TreeNode* best = find_best_child_for_max_depth(t);
        Position best_move = best->move;
        *state = play(*state, best_move.row, best_move.col);
        printf("Bot plays: %c%d\n", best_move.col + 'A', best_move.row + 1);
        return best;
    }
    else if (t->num_children == 0)
    {
        opening = false;
    }
    return t;
}

TreeNode* play_extern(State* state, TreeNode* t)
{
    char a;
    int x, y;
    bool valid_move = false;

    while (!valid_move)
    {
        printf("Play a move (use format: A1 -> H8). Enter Z0 to skip: ");
        if (scanf(" %c%d", &a, &y) != 2) 
        {
            printf("Invalid syntax! Please enter a letter (A-H) and a number (1-8), or Z0 to skip.\n");
            while (getchar() != '\n');
            continue;
        }
        if (a == 'Z' && y == 0) 
        {
            state->player = (state->player == Black) ? White : Black;
            return t;
        }

        if (a < 'A' || a > 'H' || y < 1 || y > 8)
        {
            printf("Invalid syntax! Please enter a letter (A-H) and a number (1-8).\n");
            while (getchar() != '\n');
            continue;
        }

        x = a - 'A';
        y = y - 1;

        if (x >= 0 && x < N && y >= 0 && y < N && is_move_valid(state, y, x))
        {
            valid_move = true;
        }
        else
        {
            printf("Invalid move! Please try again.\n");
        }
    }

    *state = play(*state, y, x);
    if (state->player == Black)
        {
            cur_colour = White;
        }
    else{cur_colour = Black;}

    Position played;
    played.col = x;
    played.row = y;
    bool is_child = false;
    int num_child = -1;

    FILE* f = fopen("../output.txt", "w");
    if (f == NULL) {
        printf("Error opening file.\n");
        return NULL;
    }
    fprintf(f, "%c%d\n", played.col + 'a', played.row + 1);
    fclose(f);

    if (t == NULL)
    {
        printf("Error: Tree node is NULL.\n");
        return NULL;
    }

    for (int i = 0; i < t->num_children; i++) {
        if (t->children[i]->move.col == played.col && t->children[i]->move.row == played.row) {
            is_child = true;
            num_child = i;
        }
    }
    
    if (is_child)
    {
        return t->children[num_child];
    }
    else
    {
        if (t->num_children > 0)
        {
            opening = false;
        }
        return t;
    }
}

int weight[8][8] = {
    {500, -150, 30, 10, 10, 30, -150, 500},
    {-150, -200, 0, 0, 0, 0, -200, -150},
    {30, 0, 20, 2, 2, 20, 0, 30},
    {10, 0, 2, 16, 16, 2, 0, 10},
    {10, 0, 2, 16, 16, 2, 0, 10},
    {30, 0, 20, 2, 2, 20, 0, 30},
    {-150, -200, 0, 0, 0, 0, -200, -150},
    {500, -150, 30, 10, 10, 30, -150, 500}};

int is_corner(int i, int j) {
    return (i == 0 || i == 7) && (j == 0 || j == 7);
}

int is_stable(State *state, int i, int j) {
    if (state->board[i][j] == Empty) return 0;

    int player = state->board[i][j];

    // Directions: up, down, left, right, and diagonals
    int directions[8][2] = {
        {-1, 0}, {1, 0}, {0, -1}, {0, 1}, 
        {-1, -1}, {-1, 1}, {1, -1}, {1, 1}
    };

    // If it's a corner piece, it's always stable
    if (is_corner(i, j)) return 1;

    for (int d = 0; d < 8; d++) {
        int di = directions[d][0];
        int dj = directions[d][1];
        int ni = i + di;
        int nj = j + dj;

        // Move in one direction until you hit an empty square or board edge
        while (ni >= 0 && ni < N && nj >= 0 && nj < N) {
            if (state->board[ni][nj] == Empty) return 0;
            if (state->board[ni][nj] != player) break; // stop if we hit an opponent disc
            ni += di;
            nj += dj;
        }
    }

    return 1;
}

int count_stable_pieces(State *state, Colour player) {
    int count = 0;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (state->board[i][j] == player && is_stable(state, i, j)) {
                count++;
            }
        }
    }
    return count;
}

double heur_complex(State *state) {
    if (is_term(state))
    {
        switch (winer(state))
        {
        case Black:
            return INT_MAX;
        case White:
            return INT_MIN;
        case Empty:
            return 0;
        }
    }

    int score_Black = 0, score_White = 0;
    int stable_Black = 0, stable_White = 0;
    int empty_count = 0;

    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            if (state->board[i][j] == Black)
            {
                score_Black += weight[i][j];
            }
            else if (state->board[i][j] == White)
            {
                score_White += weight[i][j];
            }
        }
    }

    // Mobility
    int move_Black[N * N][2];
    int move_White[N * N][2];
    int mobilite_Black = generer_move(state, move_Black);
    state->player = White;
    int mobilite_White = generer_move(state, move_White);
    state->player = Black;

    // Parity (favor having the last move)
    int parity = (empty_count % 2 == 0) ? 1 : -1;

    // Adjust weights based on game phase
    double early_game = (move_played < 20) ? 1.5 : 1.0;
    double late_game = (move_played > 50) ? 1.5 : 1.0;

    double weight_mobilite = 50 - move_played;
    double weight_frontier = 100;
    double weight_stability = 200;
    double weight_parity = 300;

    stable_Black = count_stable_pieces(state, Black);
    stable_White = count_stable_pieces(state, White);

    return (score_Black - score_White) * early_game
        + weight_mobilite * (mobilite_Black - mobilite_White)
        + weight_stability * (stable_Black - stable_White)
        + weight_parity * parity * late_game;
}

//-----------------------------------------------------------------------------------------------------------------


void play_egaroucid(State* state, Colour bot_colour){

    // Server Setup
    FILE* f = fopen("../command.txt", "w");
    if (f == NULL) {
        printf("Error opening file2.\n");
        return;
    }
    fprintf(f, "8.99..\n");
    fclose(f);

    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_addr_len = sizeof(client_addr);
    char recv_buf[BUFFER_SIZE];
    for (int i = 0; i < BUFFER_SIZE; i++) {
        recv_buf[i] = '\0';
    }
    char send_buf[BUFFER_SIZE];


    // 创建socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) { perror("socket"); exit(1); }

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("bind"); close(server_fd); exit(1);
    }
    if (listen(server_fd, 1) < 0) {
        perror("listen"); close(server_fd); exit(1);
    }
    printf("AI server listening on port %d...\n", PORT);
    char colour0;
    int header0 = -1;
    do{
    client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &client_addr_len);
    if (client_fd < 0) { perror("accept"); continue; }
    ssize_t n = read(client_fd, recv_buf, BUFFER_SIZE - 1);
    if (n > 0) {
        recv_buf[n] = '\0';
        printf("Received from Python: %s\n", recv_buf);
        sscanf(recv_buf, "%d|%c", &header0, &colour0);
    }
    if(header0 != 5){
        for(int i = 0; i < 4096; i+=1){send_buf[i] = recv_buf[i];}
        send_buf[0] = '4';
        send_buf[2] = '5';
        write(client_fd, send_buf, strlen(send_buf));
    }
    }while (header0 != 5);

    for(int i = 0; i < 4096; i+=1){send_buf[i] = recv_buf[i];}
        send_buf[0] = '1';
        send_buf[2] = '0';
        send_buf[3] = ' ';
        write(client_fd, send_buf, strlen(send_buf));
    close(client_fd);


    if(colour0 == 'W'){bot_colour = Black;}
    else{bot_colour = White;}
    printf("\nBot Colour : %c\n", colour0);

    //----------------------------------------


    int acutal = 1;
    char act[2] = "00";
    char last_move[2] = "00";
    char cur_move[2] = "00";
    FILE* f2 = fopen("../output.txt", "w");
    if (f2 == NULL) {
        printf("Error opening file2.\n");
        close(server_fd);
        return;
    }
    fprintf(f2, "00\n");
    fclose(f2);
    char line[100];
    char line2[100];
    int x, y;

    while (!is_term(state)) {
        printf("\nPlayer : %c\n", state->player == Black? 'B':'W');
        act[0] = '0' + (acutal / 10);
        act[1] = '0' + (acutal % 10);
        printf("\nMove number: %c%c\n", act[0], act[1]);
        if (state->player == bot_colour) {
            if(has_valid_move(state)){
                FILE* f = fopen("../command.txt", "w");
                if (f == NULL) {
                    printf("Error opening file2.\n");
                    close(server_fd);
                    return;
                }
                fprintf(f, "8.%c%c..\n", act[0], act[1]);
                fclose(f);
                last_move[0] = cur_move[0], last_move[1] = cur_move[1];
                while (last_move[0] == cur_move[0] && last_move[1] == cur_move[1]) {
                    sleep(1);
                    FILE* f2 = fopen("../output.txt", "r");
                    if (f2 == NULL) {
                        printf("Error opening file2.\n");
                        close(server_fd);
                        return;
                    }
                    if (fgets(line, sizeof(line), f2) != NULL) {
                        cur_move[0] = line[0];
                        cur_move[1] = line[1];
                    }
                    fclose(f2);
                }
                printf("Bot plays: %c%c\n", line[0], line[1]);
                x = toupper(line[0]) - 'A';
                y = line[1] - '0' - 1;
                *state = play(*state, y, x);

                int header1 = -1;
                do{
                client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &client_addr_len);
                if (client_fd < 0) { perror("accept"); continue; }
                ssize_t n = read(client_fd, recv_buf, BUFFER_SIZE - 1);
                if (n > 0) {
                    recv_buf[n] = '\0';
                    printf("Received from Python: %s\n", recv_buf);
                    sscanf(recv_buf, "%d", &header1);
                    if(header1 == 0){
                        for(int i = 0; i < 4096; i+=1){send_buf[i] = recv_buf[i];}
                        send_buf[0] = '5';
                        send_buf[2] = cur_move[0] - 32; 
                        send_buf[3] = cur_move[1];
                        write(client_fd, send_buf, strlen(send_buf));
                    }
                    else if(header1 == 6){
                        for(int i = 0; i < 4096; i+=1){send_buf[i] = recv_buf[i];}
                        send_buf[0] = '1';
                        write(client_fd, send_buf, strlen(send_buf));
                        close(client_fd);
                        close(server_fd);
                        return;
                    }
                    else{
                        for(int i = 0; i < 4096; i+=1){send_buf[i] = recv_buf[i];}
                        send_buf[0] = '4';
                        send_buf[2] = '0';
                        send_buf[3] = ' ';
                        write(client_fd, send_buf, strlen(send_buf));
                    }
                }
                close(client_fd);
                }while (header1 != 0);
            }
            print_board(state);
            acutal+=1;
            sleep(2);
            continue;
        }
        if (has_valid_move(state) && state->player != bot_colour) {
            char pos[2];
            char move[10] = {0};
            int header2;
            do{
            client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &client_addr_len);
            if (client_fd < 0) { perror("accept"); continue; }
            ssize_t n = read(client_fd, recv_buf, BUFFER_SIZE - 1);
            if (n > 0) {
                recv_buf[n] = '\0';
                printf("Received from Python: %s\n", recv_buf);
                sscanf(recv_buf, "%d", &header2);
                if(header2 == 5){
                    int header_useless;
                    int parsed = sscanf(recv_buf, "%d|%9s", &header_useless, move);
                    pos[0] = move[0];
                    pos[1] = move[1];
                    x = move[0] - 'A';
                    y = (move[1] - '0') - 1;
                    for(int i = 0; i < 4096; i+=1){send_buf[i] = recv_buf[i];}
                    send_buf[0] = '1';
                    write(client_fd, send_buf, strlen(send_buf));
                }
                else if(header2 == 6){
                    for(int i = 0; i < 4096; i+=1){send_buf[i] = recv_buf[i];}
                    send_buf[0] = '1';
                    write(client_fd, send_buf, strlen(send_buf));
                    close(client_fd);
                    close(server_fd);
                    return;
                }
                else{
                    for(int i = 0; i < 4096; i+=1){send_buf[i] = recv_buf[i];}
                    send_buf[0] = '4';
                    send_buf[2] = '5';
                    send_buf[3] = ' ';
                    write(client_fd, send_buf, strlen(send_buf));
                }
            }
            close(client_fd);
            }while (header2 != 5);

            x = move[0] - 'A';
            y = (move[1] - '0') - 1;
            printf("x = %d, y = %d\n", x, y);

            *state = play(*state, y, x);

            FILE* f3 = fopen("../output.txt", "w");
            
            if (f3 == NULL) {
                printf("Error opening file4.\n");
                close(server_fd);
                return;
            }
            else{
                fprintf(f, "%c%c\n", move[0], move[1]);
            }
            fclose(f3);

            FILE* f = fopen("../command.txt", "w");
            if (f == NULL) {
                printf("Error opening file3.\n");
                close(server_fd);
                return;
            }
            FILE* f2 = fopen("../output.txt", "r");
            
            if (f2 == NULL) {
                printf("Error opening file4.\n");
                close(server_fd);
                return;
            }
            if (fgets(line2, sizeof(line2), f2) != NULL) {
                last_move[0] = line2[0];
                last_move[1] = line2[1];
                cur_move[0] = line2[0];
                cur_move[1] = line2[1];
                fprintf(f, "5.%c%c%c%c", act[0], act[1], line2[0], line2[1]);
                fflush(f);
            } else {
                printf("Error reading line from file.\n");
            }
            fclose(f2);
            fclose(f);   
            acutal+=1;
        }
        state->player = bot_colour;        
        print_board(state);
        sleep(2.5);
    }
    while (true)
    {
        int header00;
    client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &client_addr_len);
        if (client_fd < 0) { perror("accept"); continue; }
        ssize_t n = read(client_fd, recv_buf, BUFFER_SIZE - 1);
        if (n > 0) {
            recv_buf[n] = '\0';
            printf("Received from Python: %s\n", recv_buf);
            sscanf(recv_buf, "%d", &header00);
            if(header00 == 6){
                    for(int i = 0; i < 4096; i+=1){send_buf[i] = recv_buf[i];}
                    send_buf[0] = '1';
                    write(client_fd, send_buf, strlen(send_buf));
                    close(client_fd);
                    close(server_fd);
                    return;
                }
            }
            else{
                for(int i = 0; i < 4096; i+=1){send_buf[i] = recv_buf[i];}
                    send_buf[0] = '4';
                    send_buf[3] = '6';
                    write(client_fd, send_buf, strlen(send_buf));
            }
    }
}

//-----------------------------------------------------------------------------------------------------------------

// handle the command from the client
void handle_ai_command(const char* recv_buf, char* send_buf) {
    // 解析header
    int header;
    sscanf(recv_buf, "%d", &header);
    if (header == 0) {
        // everything is fine
        strcpy(send_buf, "0");
    }
    // 根据header决定返回内容
    if (header == 1) {
        // everything is fine
        strcpy(send_buf, "1");
    } else if (header == 2) {
        // invalid move
        strcpy(send_buf, "2");
    } else if (header == 3) {
        // timeout
        strcpy(send_buf, "3 ");
    } else if (header == 4) {
        // wrong packet format
        strcpy(send_buf, "4 WRONG_PACKET_FORMAT");
    } else if (header == 5) {
        get_move(recv_buf);
        strcpy(send_buf, "5|E3|W");
    } else if (header == 6) {
        // end game
        strcpy(send_buf, "6 END_GAME");
    } else if (header == 7) {
        // resign
        strcpy(send_buf, "7 RESIGN");
    } else if (header == 8) {
        // offer draw
        strcpy(send_buf, "8 OFFER_DRAW");
    } else if (header == 9) {
        // request undo
        strcpy(send_buf, "9 REQUEST_UNDO");
    } else if (header == 10) {
        // 未知命令
        strcpy(send_buf, "10 UNKNOWN_COMMAND");
    }
}

void get_move(const char *packet) {
    int header;
    char move[10] = {0};

    int parsed = sscanf(packet, "%d|%9s", &header, move);
    if (header != 5) {
        printf("Invalid packet format or incorrect header\n");
        return;
    }
    char pos[2];
    pos[0] = move[0];
    pos[1] = move[1];
    printf("\nMove received : %c%c\n", pos[0], pos[1]);
}


int main() {

    State* state = malloc(sizeof(State)); // |
    initial(state);                       // | Initialize the board

    print_board(state);

    char *executable = "./Egaroucid_for_Console.out";
    pid_t terminal_pid = fork();

    if (terminal_pid < 0) {
        perror("Erreur fork");
        return 1;
    } else if (terminal_pid == 0) {
        // Enfant : lancer un terminal qui exécute le script
        execlp("gnome-terminal", "gnome-terminal", "--", "bash", "-c", "./start.sh", (char *)NULL);
        perror("Erreur execlp");
        exit(1);
    }

    // Parent : attendre que le script démarre
    sleep(2);

    // Lire le PID enregistré
    FILE *fp = fopen("/tmp/egaroucid.pid", "r");
    if (fp == NULL) {
        perror("Impossible de lire le fichier PID");
        return 1;
    }

    pid_t target_pid;
    fscanf(fp, "%d", &target_pid);
    fclose(fp);

    printf("PID récupéré : %d\n", target_pid);

    // Attendre avant d'envoyer SIGINT
    bot_colour = White;
    play_egaroucid(state, bot_colour);

    printf("Envoi de SIGINT (Ctrl+C) à %d\n", target_pid);
    kill(target_pid, SIGINT);

    // Optionnel : attendre que le terminal se ferme
    waitpid(terminal_pid, NULL, 0);
    
    return 0;
}