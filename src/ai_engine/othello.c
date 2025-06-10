#include "othello.h"


Colour winer(State *state)
{
    int black = 0, white = 0;
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            if (state->board[i][j] == Black)
                black++;
            else if (state->board[i][j] == White)
                white++;
        }
    }
    if (black > white)
        return Black;
    if (white > black)
        return White;
    return Empty;
}

void print_board(State *state)
{
    printf("\n  A B C D E F G H\n");
    for (int i = 0; i < N; i++)
    {
        printf("%d ", i + 1);
        for (int j = 0; j < N; j++)
        {
            char c = '.';
            if (state->board[i][j] == Black)
                c = 'B';
            else if (state->board[i][j] == White)
                c = 'W';
            printf("%c ", c);
        }
        printf("\n");
    }
    printf("\n");
}


int eval(State *state)
{
    int black = 0, white = 0;
    for (int i = 0; i < N; i += 1)
    {
        for (int j = 0; j < N; j += 1)
        {
            if (state->board[i][j] == Black)
                black += 1;
            else if (state->board[i][j] == White)
                white += 1;
        }
    }
    return black - white;
}

bool check_legal_pos(State *state, int x, int y)
{
    if (state->board[x][y] != Empty)
    {
        return false;
    }

    int directions[8][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}, {-1, -1}, {-1, 1}, {1, -1}, {1, 1}};

    Colour oponent = (state->player == Black) ? White : Black;

    for (int d = 0; d < 8; d += 1)
    {
        int dx = directions[d][0], dy = directions[d][1];
        int i = x + dx, j = y + dy;
        bool oponent_crossed = false;

        while (i >= 0 && i < N && j >= 0 && j < N)
        {
            if (state->board[i][j] == Empty)
            {
                break;
            }
            if (state->board[i][j] == oponent)
            {
                oponent_crossed = true;
            }
            else if (state->board[i][j] == state->player)
            {
                if (oponent_crossed)
                {
                    return true;
                }
                break;
            }
            i += dx;
            j += dy;
        }
    }

    return false;
}

int compute_pos(State *state, int x, int y)
{
    int pos_num = -1;
    if (x > 0)
    {
        if (state->board[x - 1][y] != Empty && state->board[x - 1][y] != state->player)
        {
            pos_num = 0;
        }
    }
    if (y > 0)
    {
        if (state->board[x][y - 1] != Empty && state->board[x][y - 1] != state->player)
        {
            pos_num = 1;
        }
    }
    if (x < 7)
    {
        if (state->board[x + 1][y] != Empty && state->board[x + 1][y] != state->player)
        {
            pos_num = 2;
        }
    }
    if (y < 7)
    {
        if (state->board[x][y + 1] != Empty && state->board[x][y + 1] != state->player)
        {
            pos_num = 3;
        }
    }
    if (x > 0 && y > 0)
    {
        if (state->board[x - 1][y - 1] != Empty && state->board[x - 1][y - 1] != state->player)
        {
            pos_num = 4;
        }
    }
    if (x < 7 && y < 7)
    {
        if (state->board[x + 1][y + 1] != Empty && state->board[x + 1][y + 1] != state->player)
        {
            pos_num = 5;
        }
    }
    if (x > 0 && y < 7)
    {
        if (state->board[x - 1][y + 1] != Empty && state->board[x - 1][y + 1] != state->player)
        {
            pos_num = 6;
        }
    }
    if (x < 7 && y > 0)
    {
        if (state->board[x + 1][y - 1] != Empty && state->board[x + 1][y - 1] != state->player)
        {
            pos_num = 7;
        }
    }
    return pos_num;
}

int is_move_valid(State *state, int x, int y)
{
    bool res = true;
    if (state->board[x][y] != Empty)
    {
        return false;
    }
    int pos_num = compute_pos(state, x, y);
    if (!(x >= 0 && x < N && y >= 0 && y < N && state->board[x][y] == Empty))
    {
        res = false;
    }

    if (pos_num == -1)
    {
        res = false;
    }
    else
    {
        res = check_legal_pos(state, x, y);
    }

    return res;
}

int generer_move(State *state, int move[N * N][2])
{
    int move_num = 0;
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            if (is_move_valid(state, i, j))
            {
                move[move_num][0] = i;
                move[move_num][1] = j;
                move_num++;
            }
        }
    }
    return move_num;
}

int is_term(State *state)
{
    int move[N * N][2];
    if (generer_move(state, move) != 0)
    {
        return 0;
    }
    State copy = *state;
    copy.player = (state->player == Black) ? White : Black;

    return generer_move(&copy, move) == 0;
}

int naive_heur(State *state)
{
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
    return eval(state);
}

int heur_points(State *state)
{
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

    int angle_score = 10;
    int side_score = 3;
    int tile_score = 1;
    int score_Black = 0;
    int score_White = 0;

    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            if (state->board[i][j] != Empty)
            {
                int *score = (state->board[i][j] == Black) ? &score_Black : &score_White;

                if ((i == 0 && j == 0) || (i == 0 && j == N - 1) ||
                    (i == N - 1 && j == 0) || (i == N - 1 && j == N - 1))
                {
                    *score += angle_score;
                }
                else if (i == 0 || j == 0 || i == N - 1 || j == N - 1)
                {
                    *score += side_score;
                }
                else
                {
                    *score += tile_score;
                }
            }
        }
    }

    return score_Black - score_White;
}




//-----------------------------------------------------------------------------------------------------------------

//-----------------------------------------------------------------------------------------------------------------


//-----------------------------------------------------------------------------------

// Min-Max Alpha-Beta
int minmax(State *state, int deapth, int alpha, int beta, int *best_x, int *best_y)
{   
    if (deapth == 0 || is_term(state))
    {
        return heur_complex(state);
    }

    int move[N * N][2];
    int move_num = generer_move(state, move);

    if (move_num == 0)
    {
        State new_state = *state;
        new_state.player = (state->player == Black) ? White : Black;
        return minmax(&new_state, deapth, alpha, beta, best_x, best_y);
    }

    if (state->player == Black)
    {
        int max_eval = INT_MIN;
        for (int i = 0; i < move_num; i++)
        {
            if (is_move_valid(state, move[i][0], move[i][1]))
            {
                State new_state = play(*state, move[i][0], move[i][1]);
                int eval = minmax(&new_state, deapth - 1, alpha, beta, NULL, NULL);
                if (eval > max_eval)
                {
                    max_eval = eval;
                    if (best_x && best_y)
                    {
                        *best_x = move[i][0];
                        *best_y = move[i][1];
                    }
                }
                alpha = (alpha > eval) ? alpha : eval;
                if (beta <= alpha)
                    break;
            }
        }
        return max_eval;
    }
    else
    {
        int min_eval = INT_MAX;
        for (int i = 0; i < move_num; i++)
        {
            if (is_move_valid(state, move[i][0], move[i][1]))
            {
                State new_state = play(*state, move[i][0], move[i][1]);
                int eval = minmax(&new_state, deapth - 1, alpha, beta, NULL, NULL);
                if (eval < min_eval)
                {
                    min_eval = eval;
                    if (best_x && best_y)
                    {
                        *best_x = move[i][0];
                        *best_y = move[i][1];
                    }
                }
                beta = (beta < eval) ? beta : eval;
                if (beta <= alpha)
                    break;
            }
        }
        return min_eval;
    }
}


double op_minmax(State *state, int deapth, int alpha, int beta, int *best_x, int *best_y)
{   
    if (deapth == 0 || is_term(state))
    {
        return naive_heur(state);
    }
    int move[N * N][2];
    int move_num = generer_move(state, move);

    if (move_num == 0)
    {
        State new_state = *state;
        new_state.player = (state->player == Black) ? White : Black;
        return op_minmax(&new_state, deapth, alpha, beta, best_x, best_y);
    }

    if (state->player == Black)
    {
        int max_eval = INT_MIN;
        for (int i = 0; i < move_num; i++)
        {
            if (is_move_valid(state, move[i][0], move[i][1]))
            {
                State new_state = play(*state, move[i][0], move[i][1]);
                int eval = op_minmax(&new_state, deapth - 1, alpha, beta, NULL, NULL);
                if (eval > max_eval)
                {
                    max_eval = eval;
                    if (best_x && best_y)
                    {
                        *best_x = move[i][0];
                        *best_y = move[i][1];
                    }
                }
                alpha = (alpha > eval) ? alpha : eval;
                if (beta <= alpha)
                    break;
            }
        }
        return max_eval;
    }
    else
    {
        int min_eval = INT_MAX;
        for (int i = 0; i < move_num; i++)
        {
            if (is_move_valid(state, move[i][0], move[i][1]))
            {
                State new_state = play(*state, move[i][0], move[i][1]);
                int eval = op_minmax(&new_state, deapth - 1, alpha, beta, NULL, NULL);
                if (eval < min_eval)
                {
                    min_eval = eval;
                    if (best_x && best_y)
                    {
                        *best_x = move[i][0];
                        *best_y = move[i][1];
                    }
                }
                beta = (beta < eval) ? beta : eval;
                if (beta <= alpha)
                    break;
            }
        }
        return min_eval;
    }
}


void give_res(State state)
{
    int nb_white = 0;
    int nb_black = 0;
    for (int i = 0; i < 8; i += 1)
    {
        for (int j = 0; j < 8; j += 1)
        {
            if (state.board[i][j] == White)
            {
                nb_white += 1;
            }
            if (state.board[i][j] == Black)
            {
                nb_black += 1;
            }
        }
    }
    if (nb_black > nb_white)
    {
        printf("\nBlack win!\nScore : %d / %d\n\n", nb_black, nb_white);
    }
    else if (nb_black < nb_white)
    {
        printf("\nWhite win!\nScore : %d / %d\n\n", nb_white, nb_black);
    }
    else
    {
        printf("\nEquality!\n\n");
    }
}

void print_bool(bool b)
{
    if (b)
    {
        printf("true\n");
    }
    else
    {
        printf("false\n");
    }
}