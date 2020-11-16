IN_CSV := $(shell find . -name coordinates.csv)
OUT_CSV = $(IN_CSV:coordinates.csv=database_entries.csv)

.PHONY: all clean

all: $(OUT_CSV)

%database_entries.csv: %coordinates.csv
	@echo Generating $@...
	$(shell python3 ./norbert_to_bob.py $< > $@)

clean:
	rm -f $(OUT_CSV)
