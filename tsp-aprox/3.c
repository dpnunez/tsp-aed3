#include <stdio.h>
#include <stdbool.h>
#include <limits.h>

#define NUM_VERTICES 15

int distances[NUM_VERTICES][NUM_VERTICES] = {
    {0, 141, 134, 152, 173, 289, 326, 329, 285, 401, 388, 366, 343, 305, 276},
    {141, 0, 152, 150, 153, 312, 354, 313, 249, 324, 300, 272, 247, 201, 176},
    {134, 152, 0, 24, 48, 168, 210, 197, 153, 280, 272, 257, 237, 210, 181},
    {152, 150, 24, 0, 24, 163, 206, 182, 133, 257, 248, 233, 214, 187, 158},
    {173, 153, 48, 24, 0, 160, 203, 167, 114, 234, 225, 210, 190, 165, 137},
    {289, 312, 168, 163, 160, 0, 43, 90, 124, 250, 264, 270, 264, 267, 249},
    {326, 354, 210, 206, 203, 43, 0, 108, 157, 271, 290, 299, 295, 303, 287},
    {329, 313, 197, 182, 167, 90, 108, 0, 70, 164, 183, 195, 194, 210, 201},
    {285, 249, 153, 133, 114, 124, 157, 70, 0, 141, 147, 148, 140, 147, 134},
    {401, 324, 280, 257, 234, 250, 271, 164, 141, 0, 36, 67, 88, 134, 150},
    {388, 300, 272, 248, 225, 264, 290, 183, 147, 36, 0, 33, 57, 104, 124},
    {366, 272, 257, 233, 210, 270, 299, 195, 148, 67, 33, 0, 26, 73, 96},
    {343, 247, 237, 214, 190, 264, 295, 194, 140, 88, 57, 26, 0, 48, 71},
    {305, 201, 210, 187, 165, 267, 303, 210, 147, 134, 104, 73, 48, 0, 30},
    {276, 176, 181, 158, 137, 249, 287, 201, 134, 150, 124, 96, 71, 30, 0}
};

int minKey(int key[], bool mstSet[]) {
    int min = INT_MAX, min_index;

    for (int v = 0; v < NUM_VERTICES; v++) {
        if (mstSet[v] == false && key[v] < min) {
            min = key[v];
            min_index = v;
        }
    }

    return min_index;
}

void printMST(int parent[], int graph[NUM_VERTICES][NUM_VERTICES]) {
    printf("Caminho do Caixeiro Viajante:\n");
    printf("0 -> ");
    for (int i = 1; i < NUM_VERTICES; i++) {
        printf("%d -> ", parent[i]);
    }
    printf("0\n");

    int totalCost = 0;
    for (int i = 0; i < NUM_VERTICES - 1; i++) {
        totalCost += graph[parent[i]][i];
    }
    printf("Custo Total: %d\n", totalCost);
}

void treeTSP() {
    int parent[NUM_VERTICES];
    int key[NUM_VERTICES];
    bool mstSet[NUM_VERTICES];

    for (int i = 0; i < NUM_VERTICES; i++) {
        key[i] = INT_MAX;
        mstSet[i] = false;
    }

    key[0] = 0;
    parent[0] = -1;

    for (int count = 0; count < NUM_VERTICES - 1; count++) {
        int u = minKey(key, mstSet);
        mstSet[u] = true;

        for (int v = 0; v < NUM_VERTICES; v++) {
            if (distances[u][v] && mstSet[v] == false && distances[u][v] < key[v]) {
                parent[v] = u;
                key[v] = distances[u][v];
            }
        }
    }

    printMST(parent, distances);
}

int main() {
    treeTSP();

    return 0;
}
