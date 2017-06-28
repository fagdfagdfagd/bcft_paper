#!/bin/bash

# remove the tex file extention except for the master file bCFT.tex
# then compress to tar gz that can be uploaded to arxiv
tar --transform='flags=r;s|.tex||' --transform='flags=r;s|^bCFT$|bCFT.tex|' -cvzf bCFT.tar.gz *.tex *.bbl images