#include "othello.h"

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
void play_heur_naive(State *state, TreeNode *root, Colour bot_colour)
{
    TreeNode* current_node = root;
    int best_x = -1, best_y = -1;
    int stalemate_counter = 0;

    while (!is_term(state))
        {

            int move[N * N][2];
            int move_num = generer_move(state, move);
            
            if (move_num == 0) {
                printf("Player %c has no valid moves. Switching player.\n", 
                    (state->player == Black) ? 'B' : 'W');
                state->player = (state->player == Black) ? White : Black;
                stalemate_counter++;
                continue;
            }
            
            stalemate_counter = 0;
            if (state->player == bot_colour)
            {
                
                if (opening && current_node->num_children > 0)
                {
                    current_node = play_opening(state, current_node);
                }
                else
                {
                    if (opening) {
                        opening = false;
                        root = NULL;
                        current_node = NULL;
                    }
                    
                    op_minmax(state, 8, INT_MIN, INT_MAX, &best_x, &best_y);
                    
                    if (is_move_valid(state, best_x, best_y)) {
                        printf("Bot plays: %c%d\n", best_y + 'A', best_x + 1);
                        *state = play(*state, best_x, best_y);
                    } else {
                        bool found_valid_move = false;
                        for (int i = 0; i < move_num; i++) {
                            if (is_move_valid(state, move[i][0], move[i][1])) {
                                best_x = move[i][0];
                                best_y = move[i][1];
                                found_valid_move = true;
                                printf("Bot plays alternative move: %c%d\n", best_y + 'A', best_x + 1);
                                *state = play(*state, best_x, best_y);
                                break;
                            }
                        }
                        
                        if (!found_valid_move) {
                            printf("Bot couldn't find any valid move. Switching player.\n");
                            state->player = (state->player == Black) ? White : Black;
                            continue;
                        }
                    }
                }
            }
        else
        {
            current_node = play_extern(state, current_node);
        }
        if(!opening)
        {
            move_played+=1;
        }
        print_board(state);
    }
}
//-----------------------------------------------------------------------------------------------------------------
void play_heur_complex(State *state, TreeNode *root, Colour bot_colour)
{
    TreeNode* current_node = root;
    int best_x = -1, best_y = -1;
    int stalemate_counter = 0;

    while (!is_term(state))
        {

            int move[N * N][2];
            int move_num = generer_move(state, move);
            
            if (move_num == 0) {
                printf("Player %c has no valid moves. Switching player.\n", 
                    (state->player == Black) ? 'B' : 'W');
                state->player = (state->player == Black) ? White : Black;
                stalemate_counter++;
                continue;
            }
            
            stalemate_counter = 0;
            if (state->player == bot_colour)
            {
                
                if (opening && current_node->num_children > 0)
                {
                    current_node = play_opening(state, current_node);
                }
                else
                {
                    if (opening) {
                        opening = false;
                        root = NULL;
                        current_node = NULL;
                    }
                    
                    minmax(state, 8, INT_MIN, INT_MAX, &best_x, &best_y);
                    
                    if (is_move_valid(state, best_x, best_y)) {
                        printf("Bot plays: %c%d\n", best_y + 'A', best_x + 1);
                        *state = play(*state, best_x, best_y);
                    } else {
                        bool found_valid_move = false;
                        for (int i = 0; i < move_num; i++) {
                            if (is_move_valid(state, move[i][0], move[i][1])) {
                                best_x = move[i][0];
                                best_y = move[i][1];
                                found_valid_move = true;
                                printf("Bot plays alternative move: %c%d\n", best_y + 'A', best_x + 1);
                                *state = play(*state, best_x, best_y);
                                break;
                            }
                        }
                        
                        if (!found_valid_move) {
                            printf("Bot couldn't find any valid move. Switching player.\n");
                            state->player = (state->player == Black) ? White : Black;
                            continue;
                        }
                    }
                }
            }
        else
        {
            current_node = play_extern(state, current_node);
        }
        if(!opening)
        {
            move_played+=1;
        }
        print_board(state);
    }
}
//-----------------------------------------------------------------------------------------------------------------
void play_egaroucid(State* state, Colour bot_colour){
    int acutal = 1;
    char act[2] = "00";
    char last_move[2] = "00";
    char cur_move[2] = "00";
    FILE* f = fopen("../command.txt", "w");
    if (f == NULL) {
        printf("Error opening file2.\n");
        return;
    }
    fprintf(f, "8.99..\n");
    fclose(f);
    FILE* f2 = fopen("../output.txt", "w");
    if (f2 == NULL) {
        printf("Error opening file2.\n");
        return;
    }
    fprintf(f2, "00\n");
    fclose(f2);
    char line[100];
    char line2[100];
    int x, y;
    while (true) {
        act[0] = '0' + (acutal / 10);
        act[1] = '0' + (acutal % 10);
        if (state->player == bot_colour) {
            FILE* f = fopen("../command.txt", "w");
            if (f == NULL) {
                printf("Error opening file2.\n");
                return;
            }
            fprintf(f, "8.%c%c..\n", act[0], act[1]);
            fclose(f);
            while (last_move[0] == cur_move[0] && last_move[1] == cur_move[1]) {
                sleep(1);
                FILE* f2 = fopen("../output.txt", "r");
                if (f2 == NULL) {
                    printf("Error opening file2.\n");
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
            if(state->player == bot_colour)
            {
                state->player = (state->player == Black) ? White : Black;
            }
            
        } else {
            play_extern(state, NULL);
            FILE* f = fopen("../command.txt", "w");
            if (f == NULL) {
                printf("Error opening file3.\n");
                return;
            }
            FILE* f2 = fopen("../output.txt", "r");
            
            if (f2 == NULL) {
                printf("Error opening file4.\n");
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
        }
        print_board(state);
        acutal+=1;
        sleep(3);
    }
}
//-----------------------------------------------------------------------------------------------------------------

int main()
{

    TreeNode *root = build_tree_from_file("ouvertures2.txt");
    if (root == NULL) {
        return EXIT_FAILURE;
    }
    State* state = malloc(sizeof(State));
    initial(state);
    printf("Select the colour of the bot (B/W): ");
    char c;
    scanf(" %c", &c);
    if (c == 'B' || c == 'b') {
        bot_colour = Black;
    } else if (c == 'W' || c == 'w') {
        bot_colour = White;
    } else {
        printf("Invalid input. Exiting.\n");
        free_tree(root);
        free(state);
        return EXIT_FAILURE;
    }

    printf("Select the difficulty level of the bot (1 to 3): ");
    int d;
    scanf(" %d", &d);   
    
    print_board(state);

    if (d == 3){
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
        play_egaroucid(state, bot_colour);

        printf("Envoi de SIGINT (Ctrl+C) à %d\n", target_pid);
        kill(target_pid, SIGINT);

        // Optionnel : attendre que le terminal se ferme
        waitpid(terminal_pid, NULL, 0);
    }
    if (d == 2)
    {
        play_heur_complex(state, root, bot_colour);
    }

    if (d == 1)
    {
        play_heur_naive(state, root, bot_colour);
    }
    
    else {
        printf("Invalid input. Exiting.\n");
        free_tree(root);
        free(state);
        return EXIT_FAILURE;
    }

    give_res(*state);

    free_tree(root);
    free(state);
    return 0;
}
//Format : XXYYZZ | XX : Commande | YY (5. pour play, 8. pour go et 12 pour mode) : Numéro du coup | ZZ : Argument