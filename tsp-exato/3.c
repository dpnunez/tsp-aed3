#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <limits.h>
#include <time.h>

#define MAX_CITIES 15

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