#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <limits.h>
#include <time.h>

#define MAX_CITIES 11

int tsp_brute_force(int distances[MAX_CITIES][MAX_CITIES], int num_cities, int* best_path) {
    int cities[MAX_CITIES];
    int i, j, k;
    int best_distance = INT_MAX;

    for (i = 0; i < num_cities; i++) {
        cities[i] = i;
    }

    do {
        int current_distance = 0;
        for (i = 0; i < num_cities - 1; i++) {
            current_distance += distances[cities[i]][cities[i+1]];
        }
        current_distance += distances[cities[num_cities-1]][cities[0]];

        if (current_distance < best_distance) {
            best_distance = current_distance;
            for (j = 0; j < num_cities; j++) {
                best_path[j] = cities[j];
            }
        }
    } while (next_permutation(cities, num_cities));

    return best_distance;
}

void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int next_permutation(int* array, int length) {
    int i = length - 2;
    while (i >= 0 && array[i] > array[i + 1]) {
        i--;
    }
    if (i < 0) {
        return 0;
    }
    int j = length - 1;
    while (array[i] > array[j]) {
        j--;
    }
    swap(&array[i], &array[j]);
    int left = i + 1;
    int right = length - 1;
    while (left < right) {
        swap(&array[left], &array[right]);
        left++;
        right--;
    }
    return 1;
}

int main() {
    int distances[MAX_CITIES][MAX_CITIES] = {
        {0, 29, 20, 21, 16, 31, 100, 12, 4, 31, 18},
        {29, 0, 15, 29, 28, 40, 72, 21, 29, 41, 12},
        {20, 15, 0, 15, 14, 25, 81, 9, 23, 27, 13},
        {21, 29, 15, 0, 4, 12, 92, 12, 25, 13, 25},
        {16, 28, 14, 4, 0, 16, 94, 9, 20, 16, 22},
        {31, 40, 25, 12, 16, 0, 95, 24, 36, 3, 37},
        {100, 72, 81, 92, 94, 95, 0, 90, 101, 99, 84},
        {12, 21, 9, 12, 9, 24, 90, 0, 15, 25, 13},
        {4, 29, 23, 25, 20, 36, 101, 15, 0, 35, 18},
        {31, 41, 27, 13, 16, 3, 99, 25, 35, 0, 38},
        {18, 12, 13, 25, 22, 37, 84, 13, 18, 38, 0}
    };

    int best_path[MAX_CITIES];
    int best_distance;

    clock_t start_time = clock();

    best_distance = tsp_brute_force(distances, MAX_CITIES, best_path);

    printf("Melhor caminho: ");
    for (int i = 0; i < MAX_CITIES; i++) {
        printf("%d ", best_path[i]);
    }
    printf("\nDistância total: %d\n", best_distance);

    double elapsed_time = (double)(clock() - start_time) / CLOCKS_PER_SEC;
    printf("--- %.6f seconds ---\n", elapsed_time);

    return 0;
}