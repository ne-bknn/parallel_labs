#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void new_array(int *, unsigned int *, int);

void new_array(int *array, unsigned int *random_seed, int count) {
  srand(*random_seed);
  int i;
  int threads = 16;
  int chunk = count / threads;
#pragma omp parallel for shared(array, count, chunk) default(none) private(i)  \
    schedule(dynamic, chunk) num_threads(threads)
  for (i = 0; i < count; i++) {
    array[i] = rand();
  }
  *random_seed += rand();
}

int main() {
  const int count = 10000000;
  unsigned int random_seed = 920214;
  const int num_exp = 20;
  const int thread_bound = 100;

  int **arrays = NULL;
  int *array = NULL;
  int index, i, target, threads;

  double t1, t2, res;

  arrays = (int **)calloc(num_exp, sizeof(int *));
  for (int t = 0; t < num_exp; t++) {
    array = (int *)calloc(count, sizeof(int));
    new_array(array, &random_seed, count);
    arrays[t] = array;
  }

  for (threads = 1; threads <= thread_bound; threads++) {
    fprintf(stderr, "curthreads: %d\n", threads);
    res = 0.0;
    for (int j = 0; j < num_exp; j++) {
      target = arrays[j][rand() % count];
      index = count + 1;

      t1 = omp_get_wtime();
#pragma omp parallel for shared(arrays, count, target, j) default(             \
    none) private(i) num_threads(threads) reduction(min                        \
                                                    : index)
      for (i = 0; i < count; i++) {

        if (arrays[j][i] == target) {
          index = i;
        }
      }
      t2 = omp_get_wtime();
      res += t2 - t1;
    }
    res /= (double)(num_exp);
    fprintf(stdout, "(%d, %g), ", threads, res);
  }

  for (int t = 0; t < num_exp; t++) {
    free(arrays[t]);
  }
  free(arrays);
  return (0);
}
