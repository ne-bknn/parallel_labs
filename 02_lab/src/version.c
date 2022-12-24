#include <omp.h>
#include <stdio.h>

int main() {
  switch (_OPENMP) {
    case 200505:
      printf("OpenMP 2.5\n");
      break;

    case 200805:
      printf("OpenMP 3.0\n");
      break;

    case 201107:
      printf("OpenMP 3.1\n");
      break;

    case 201307:
      printf("OpenMP 4.0\n");
      break;

    case 201511:
      printf("OpenMP 4.5\n");
      break;

    case 201811:
      printf("OpenMP 5.0\n");
      break;

    default:
      printf("Unknown\n");
  }
}
