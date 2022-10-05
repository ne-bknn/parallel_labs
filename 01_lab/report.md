# НИЯУ МИФИ. Лабораторная работа №1. Мищенко Тимофей, Б20-505. 2022

## Система

### Характеристики процессора:
```
CPU:
  Info: quad core model: Intel Core i5-8265U bits: 64 type: MT MCP cache:
    L2: 1024 KiB
  Speed (MHz): avg: 1392 min/max: 400/3900 cores: 1: 1001 2: 938 3: 1800
    4: 1000 5: 1000 6: 1800 7: 1800 8: 1800
```

### Характеристики памяти:
```
Machine:
  Type: Laptop System: LENOVO product: 20NX000ART v: ThinkPad T490s
    serial: <superuser required>
  Mobo: LENOVO model: 20NX000ART v: SDK0J40697 WIN
    serial: <superuser required> UEFI: LENOVO v: N2JET94W (1.72 )
    date: 03/03/2021
```

### Версия gcc:
```
gcc (GCC) 12.2.0
```

### Версия OpenMP:
```
OpenMP 4.5
```

### Остальные Характеристики
```
5.19.12-arch1-1 x86_64
```

## Оценка алгоритма

### Блок-схема

```mermaid
    %%{ init : {"flowchart" : { "curve" : "stepAfter" }}}%%
    %%| fig-width: 7
    graph TD
        A(start) --> B(i: 0 -> n)
        
        B --> C{"array[i] > max"}
        B --> E(exit)
        C -->|yes| D["max = array[i]"]
        D --> B
        C -->|no| B
```

### Принцип работы
Приведенный алгоритм итерируется по массиву чисел и сравнивает их с текущим для данного потока 
максимальным элементом - max. Если элемент оказывается больше чем max, то max присваивается значение
этого элемнта, иначе не присваивается. После выполнения итерационной части потока,
полученное внутри потока значение max сравнивается с max из shared области и из них
выбирается наибольший. В итоге наибольший элемент будет в переменной max из shared области. 

### Оценка сложности алгоритмы

$p$ - количество используемых потоков  
$n$ - длина обрабатываемой последовательности

Тогда, сложность алгоритма - $O(\frac{n}{p})$; в частности, при $p = 1$, сложность - $O(n)$.

Теоретическое, ускорение работы программы - $p$.

### Директивы OpenMP
`#pragma omp parallel num_threads(threads) shared(array, count) reduction(max: max) default(none)`  
Объявляется параллельная обасть, с количеством потоков `threads`. Переменные `array` и `count`
объявляются общими для всех потокв и непараллельной части алгоритма. Все новые переменные без явного
указания класса не разрешены.  
Область - цикл for.
Если бы ее не было то цикл просто выполнился бы последовательно.

`#pragma omp for`
Задается директива относящаяся к циклу for идущему сразу после нее, выполняется распараллеливагие цикла с дефолтным значением schedule.
Область - цикл for.  
Если бы ее не было то цикл выполнился бы `threads` раз, каждый раз находя один и тот же максимальный элемент.

### Экспериментальные данные

Время работы программы при различном количестве потоков

![image](target/threads.png)

Ускорение работы программы по сравнению с однопоточной версией

![image](target/acceleration.png)

Эффективность работы программы

![image](target/efficiency.png)

## Выводы
На устройстве, на котором проходило тестирование - 4 физических ядра, из-за чего значительный
прирост программа показывает только при использовании 2 потоков. Вплоть до 8 потоков скорость выполнения
уменьшается, но с сильным отрывом от теоретической скорости выполнения. Использование больше чем 8 потоков 
не дает прироста в скорости выполнения программы.

## Исходный код

```c 
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
```
