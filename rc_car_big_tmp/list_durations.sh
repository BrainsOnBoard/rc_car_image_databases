#!/bin/bash

for d in $@; do
	printf "%s:	%.2f\n" "$d" $(bc <<< "`tail -n1 $d/database_entries.csv |cut -f1 -d,` / 1000.0")
done
