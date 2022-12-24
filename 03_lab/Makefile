CC=gcc

ASAN=-fsanitize=address
ASAN += -fno-common
ASAN += -fno-omit-frame-pointer

CFLAGS = -Wall
CFLAGS += -Wextra

DEBUG = -g

OPENMP = -fopenmp

.PHONY: report
report.md: trace.txt target/version graphs src/report.md.jinja2
	../utils/render src/$@.jinja2 > $@

target:
	mkdir -p $@

main: target/main

trace.txt: target/main
	./target/main

.PHONY: graphs
graphs: trace.txt
	python src/graph.py

target/main: src/main.c | target
	$(CC) $(OPENMP) $(DEBUG) $(CFLAGS) $(ASAN) $? -o $@

target/version: src/version.c | target
	$(CC) $(OPENMP) $? -o $@

.PHONY: clean
clean:
	-@rm target/* 2> /dev/null
	-@rm report.md 2> /dev/null 
