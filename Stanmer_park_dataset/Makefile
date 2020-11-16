IN_CSV := $(shell find . -name coordinates.csv)
OUT_CSV := $(IN_CSV:coordinates.csv=database_entries.csv)
METADATA := $(IN_CSV:coordinates.csv=database_metadata.yaml)

.PHONY: all clean database_entries database_metadata

all: database_entries database_metadata

database_entries: $(OUT_CSV)

%database_entries.csv: %coordinates.csv
	@echo Generating $@...
	$(shell python3 ./norbert_to_bob.py $< > $@)

database_metadata: $(METADATA)

%.yaml: metadata_template.yaml
	@echo Generating $@...
	@cp -f $< $@

clean:
	rm -f $(OUT_CSV)
