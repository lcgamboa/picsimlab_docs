
VERSION=0.8.9

all:
	pdflatex -shell-escape  picsimlab.tex
	#bibtex picsimlab
	#pdflatex picsimlab.tex
	pdflatex -shell-escape  picsimlab.tex
	evince picsimlab.pdf &

clean:
	rm -f *.log *.dvi *.lof *.lot *.toc *.aux *.ps *.pdf *.out *.bbl *.blg *.maf *.mtc* *.ptc*
	rm -f *.backup *.bak *.*~ *.html *.4ct *.4tc *.idv *.tmp *.xref *.lg
	rm -fr picsimlab/ _minted-picsimlab/


html_old:
	rm -fr picsimlab/
	latex2html -split +3 -link 3 -info 0 -white -long_titles 4 -html_version 4.0,unicode -local_icons -image_type png picsimlab.tex 
	cd picsimlab && rm -f *.log *.pl *.lof *.lot *.toc *.aux *.tex WARNINGS *.out *.bbl *.blg *.maf *.mtc* *.ptc*
	firefox picsimlab/picsimlab.html &

install: all html
	install -d ../${VERSION}
	rm -fr ../${VERSION}/*.html ../${VERSION}/*.png ../${VERSION}*/.css ../${VERSION}/*.pdf
	cp picsimlab.pdf ../${VERSION}/
	cd picsimlab && cp -r * ../../${VERSION}/
	cp ../${VERSION}/picsimlab.html ../${VERSION}/index.html

#https://tex.stackexchange.com/questions/237566/best-workflows-or-tools-to-generate-an-html-web-page-from-a-complex-latex-docume
#https://github.com/michal-h21/reyman
html:
	rm -fr picsimlab/
	make4ht -c config.cfg -s -d picsimlab -f html5+common_domfilters -e build.mk4  picsimlab.tex "4,sec-filename" 
	rm -rf *.html *.aux
	sed -i "s/<main class='main-content'>//g" picsimlab/picsimlab.html
	sed -i "s/<\/main>//g" picsimlab/picsimlab.html
	cp picsimlab.js picsimlab/
	firefox picsimlab/picsimlab.html &

