CC=mpiCC

main: src/main.cpp
	$(CC) $^ -g -o $@

.PHONY: report.md
report.md: src/report.md.jinja2
	../utils/render src/$@.jinja2 > $@

.PHONY: clean
clean:
	-@rm target/* 2> /dev/null
	-@rm report.md 2> /dev/null 
