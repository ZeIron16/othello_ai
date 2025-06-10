#ifndef OTHELLO
#define OTHELLO

#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>



#define N 8
#define MAX_LINE_LENGTH 256
#define MAX_MOVES 64

typedef enum
{
    Empty,
    Black,
    White
} Colour;

typedef struct
{
    Colour player;
    Colour board[N][N];
} State;

//-----------------------------------------------------

typedef struct {
    char col;
    int row;
} Position;

typedef struct TreeNode {
    Position move;            
    struct TreeNode **children; 
    int num_children; 
} TreeNode;

//-----------------------------------------------------

TreeNode* create_node(Position move);
void add_child(TreeNode *parent, TreeNode *child);
Position parse_position(const char *notation);
TreeNode* find_child(TreeNode *node, Position move);
TreeNode* build_tree_from_file(const char *filename);
void position_to_string(Position pos, char *buffer);
TreeNode* find_deepest_leaf(TreeNode *node, int *max_depth, int current_depth);
TreeNode* find_best_child_for_max_depth(TreeNode *node);
void free_tree(TreeNode *node);

void print_tree(TreeNode *node, int depth);

//-----------------------------------------------------

Colour winer(State *state);
void print_board(State *state);
int eval(State *state);
bool check_legal_pos(State *state, int x, int y);
int compute_pos(State *state, int x, int y);
int is_move_valid(State *state, int x, int y);
int is_term(State *state);
int naive_heur(State *state);
int heur_points(State *state);
double heur_complex(State *state);
State play(State state, int x, int y);
int minmax(State *state, int deapth, int alpha, int beta, int *best_x, int *best_y);
double op_minmax(State *state, int deapth, int alpha, int beta, int *best_x, int *best_y);
void give_res(State state);
void print_bool(bool b);
int generer_move(State *state, int move[N * N][2]);



#endif