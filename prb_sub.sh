#!/bin/bash

./flatex -v bCFT.tex
tar --transform='flags=r;s|.flt|.tex|' -cvzf bCFT.tar.gz bCFT.flt images *.bbl