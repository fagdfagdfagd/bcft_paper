#!/bin/bash

# remove the tex file extention except for the master file bCFT_paper.tex
# then compress to tar gz that can be uploaded to arxiv
tar --transform='flags=r;s|.tex||' --transform='flags=r;s|^bCFT_paper$|bCFT_paper.tex|' -cvzf bCFT_paper.tar.gz *.tex *.bbl images