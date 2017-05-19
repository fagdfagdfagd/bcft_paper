#!/bin/bash

for file in *.txt; do
	filename="${file%.*}"
	mv $file $filename
done