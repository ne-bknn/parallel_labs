#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

void randomize_array(int *array, const int random_seed, int count) {
    for (int i = 0; i < count; i++) {
	array[i] = rand();
    }
}

int main(int argc, char **argv) {
    if (argc != 4) {
	printf("Usage: %s <n_threads> <random_seed> <n_times>\n", argv[0]);
	return 1;
    }

    const int count = 10000000;
    const int threads = atoi(argv[1]);
    const int random_seed = atoi(argv[2]);
    const int n_times = atoi(argv[3]);

    srand(random_seed);

    int *array = calloc(count, sizeof(int));
    int max = -1;

    for (int i = 0; i < n_times; i++) {
        randomize_array(array, random_seed, count);
        double start = omp_get_wtime();
        #pragma omp parallel num_threads(threads) shared(array, count) reduction(max: max) default(none)
        {
            #pragma omp for
            for (int i = 0; i < count; i++) {
            if (array[i] > max) {
                max = array[i];
            };
            }
        }
        double end = omp_get_wtime();
        printf("%g\n", end - start);
    }

    free(array);

    return 0;
}
