#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <limits.h>
#include <time.h>

#define MAX_CITIES 6

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
        {0, 64, 378, 519, 434, 200},
				{64, 0, 318, 455, 375, 164},
				{378, 318, 0, 170, 265, 344},
				{519, 455, 170, 0, 223, 428},
				{434, 375, 265, 223, 0, 273},
				{200, 164, 344, 428, 273, 0}
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