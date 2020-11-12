IN_CSV := $(shell find -name coordinates.csv)
OUT_CSV = $(IN_CSV:coordinates.csv=database_entries.csv)

.PHONY: all

all: $(OUT_CSV)

%database_entries.csv: %coordinates.csv
	$(shell python3 ./norbert_to_bob.py $< > $@)
