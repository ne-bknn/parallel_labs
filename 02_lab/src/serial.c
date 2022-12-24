#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

void new_array(int *, unsigned int *, int);

void new_array(int *array, unsigned int *random_seed, int count) {
  srand(*random_seed);
  int i;
  int chunk = count / 16;
  int threads = 16;
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

  int *array = 0;
  int index;

  srand(random_seed);

  array = (int *)malloc(count * sizeof(int));

  int target;
  double t1, t2, res = 0.0;

  for (int i = 0; i < num_exp; i++) {
    printf("started array\n");
    new_array(array, &random_seed, count);
    printf("ended array\n");
    target = array[rand() % count];
    t1 = omp_get_wtime();
    index = -1;
    for (int i = 0; i < count; i++) {
      if (array[i] == target) {
        index = i;
        break;
      }
    }
    t2 = omp_get_wtime();
    res += t2 - t1;
  }
  res /= (double)(num_exp);
  printf("Average time: %g\n", res);

  free(array);
  return (0);
}
