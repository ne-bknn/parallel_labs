.PHONY: report
report.md: src/report.md.jinja2
	../utils/render src/$@.jinja2 > $@

.PHONY: clean
clean:
	-@rm target/* 2> /dev/null
	-@rm report.md 2> /dev/null 
