#!/bin/bash

./flatex -v -b bCFT_paper.tex
tar --transform='flags=r;s|.flt|.tex|' -cvzf bCFT_paper.tar.gz bCFT_paper.flt images *.bbl