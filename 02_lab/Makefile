CC=gcc

ASAN=-fsanitize=address
ASAN += -fno-common
ASAN += -fno-omit-frame-pointer

CFLAGS = -Wall
CFLAGS += -Wextra

DEBUG = -g

OPENMP = -fopenmp

AVG = graphs/AvgTime.png
ACC = graphs/Acceleration.png
EFF = graphs/Efficiency.png

.PHONY: all
all: parallel.out serial.out report.md

report.md: target/version src/report.md.jinja2 graphs
	echo "Creating report"
	../utils/render src/$@.jinja2 > $@

.PHONY: graphs
graphs: serial.out parallel.out graphs/graph.py
	@printf "t_succ = " > graphs/timing.py
	@./serial.out >> graphs/timing.py
	@printf "\nts = [" >> graphs/timing.py
	@./parallel.out >> graphs/timing.py
	@printf "]\n" >> graphs/timing.py
	@python graphs/graph.py $(AVG) $(ACC) $(EFF)

parallel.out: ./src/parallel.c
	@echo Building parallel
	@$(CC) $(CFLAGS) $(ASAN) $^ -o $@ $(OPENMP)

serial.out: ./src/serial.c
	@echo Building serial
	@$(CC) $(CFLAGS) $(ASAN) $^ -o $@ $(OPENMP)

target:
	mkdir -p $@

target/version: src/version.c | target
	$(CC) $(OPENMP) $? -o $@

.PHONY: clean
clean:
	-@rm target/* 2> /dev/null
	-@rm report.md 2> /dev/null 
