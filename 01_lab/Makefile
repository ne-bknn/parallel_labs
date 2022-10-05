CC=gcc

ASAN=-fsanitize=address
ASAN += -fno-common
ASAN += -fno-omit-frame-pointer

CFLAGS = -Wall
CFLAGS += -Wextra

DEBUG = -g

OPENMP = -fopenmp

.PHONY: report
report.md: target/version target/main src/report.md.jinja2 benchmark
	../utils/render src/$@.jinja2 > $@

target:
	mkdir -p $@

.PHONY: main
main: target/main

.PHONY: benchmark
benchmark: src/benchmark.py 
	python3 $?

target/main: src/main.c | target
	$(CC) $(OPENMP) $(DEBUG) $(CFLAGS) $(ASAN) $? -o $@

target/version: src/version.c | target
	$(CC) $(OPENMP) $? -o $@

.PHONY: clean
clean:
	-@rm target/* 2> /dev/null
	-@rm report.md 2> /dev/null 
