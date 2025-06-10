#include "othello.h"

TreeNode* create_node(Position move) {
    TreeNode *node = (TreeNode*)malloc(sizeof(TreeNode));
    node->move = move;
    node->children = NULL;
    node->num_children = 0;
    return node;
}

void add_child(TreeNode *parent, TreeNode *child) {
    parent->num_children++;
    parent->children = (TreeNode**)realloc(parent->children, parent->num_children * sizeof(TreeNode*));
    parent->children[parent->num_children - 1] = child;
}

Position parse_position(const char *notation) {
    Position pos;
    pos.col = toupper(notation[0]) - 'A';
    pos.row = notation[1] - '1';
    return pos;
}

TreeNode* find_child(TreeNode *node, Position move) {
    for (int i = 0; i < node->num_children; i++) {
        if (node->children[i]->move.col == move.col && node->children[i]->move.row == move.row) {
            return node->children[i];
        }
    }
    return NULL;
}

TreeNode* build_tree_from_file(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Impossible d'ouvrir le fichier");
        return NULL;
    }

    TreeNode *root = create_node((Position){-1, -1});
    char line[MAX_LINE_LENGTH];

    while (fgets(line, MAX_LINE_LENGTH, file)) {
        line[strcspn(line, "\n")] = 0;

        char *options_start = strchr(line, '{');
        if (!options_start) continue;

        *options_start = '\0';
        char *sequence = line;
        char *options = options_start + 1;
        options[strlen(options) - 1] = '\0';

        TreeNode *current = root;
        char *token = strtok(sequence, " ");
        char move[3];
        int i = 0;

        while (token && sscanf(token + i, "%2s", move) == 1) {
            Position pos = parse_position(move);
            TreeNode *child = find_child(current, pos);
            if (!child) {
                child = create_node(pos);
                add_child(current, child);
            }
            current = child;
            i += 2;
            if (strlen(token) <= i) break;
        }

        char *option = strtok(options, ", ");
        while (option) {
            Position pos = parse_position(option);
            TreeNode *child = find_child(current, pos);
            if (!child) {
                add_child(current, create_node(pos));
            }
            option = strtok(NULL, ", ");
        }
    }

    fclose(file);
    return root;
}

void position_to_string(Position pos, char *buffer) {
    if (pos.col >= 0 && pos.row >= 0) {
        sprintf(buffer, "%c%d", 'A' + pos.col, pos.row + 1);
    } else {
        strcpy(buffer, "Invalid");
    }
}

void print_tree(TreeNode *node, int depth) {
    if (node == NULL) return;

    if (node->num_children > 0) {
        char pos_str[4];
        position_to_string(node->move, pos_str);
        printf("Coup possible à partir de %s : ", pos_str);
        for (int i = 0; i < node->num_children; i++) {
            position_to_string(node->children[i]->move, pos_str);
            printf("%s", pos_str);
            if (i < node->num_children - 1) printf(", ");
        }
        printf("\n");
    }

    for (int i = 0; i < node->num_children; i++) {
        print_tree(node->children[i], depth + 1);
    }
}

TreeNode* find_deepest_leaf(TreeNode *node, int *max_depth, int current_depth) {
    if (node == NULL) return NULL;

    if (node->num_children == 0) {
        if (current_depth > *max_depth) {
            *max_depth = current_depth;
            return node;
        }
        return NULL;
    }

    TreeNode *deepest_node = NULL;
    for (int i = 0; i < node->num_children; i++) {
        int depth = *max_depth;
        TreeNode *child_deepest = find_deepest_leaf(node->children[i], &depth, current_depth + 1);
        if (depth > *max_depth) {
            *max_depth = depth;
            deepest_node = child_deepest;
        }
    }

    return deepest_node;
}

TreeNode* find_best_child_for_max_depth(TreeNode *node) {
    if (node == NULL || node->num_children == 0) return NULL;

    int max_depth = 0;
    TreeNode *best_child = NULL;

    for (int i = 0; i < node->num_children; i++) {
        int child_max_depth = 0;
        find_deepest_leaf(node->children[i], &child_max_depth, 1);
        if (child_max_depth > max_depth) {
            max_depth = child_max_depth;
            best_child = node->children[i];
        }
    }

    return best_child;
}

void free_tree(TreeNode *node) {
    if (node == NULL) return;

    for (int i = 0; i < node->num_children; i++) {
        free_tree(node->children[i]);
    }

    free(node->children);

    free(node);
}
