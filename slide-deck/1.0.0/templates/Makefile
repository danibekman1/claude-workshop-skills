PLOTS  := $(wildcard plots/*.py)
PLOTS  := $(filter-out plots/_common.py,$(PLOTS))
FIGS   := $(patsubst plots/%.py,figs/%.png,$(PLOTS))

PANDOC_FLAGS := -t beamer --slide-level=2 \
                -V theme:metropolis -V aspectratio:169 -V fontsize:10pt \
                --pdf-engine=xelatex \
                --include-in-header=theme-overrides.tex

slides.pdf: slides.md theme-overrides.tex $(FIGS)
	pandoc slides.md $(PANDOC_FLAGS) -o slides.pdf

notes.pdf: slides.md theme-overrides.tex notes-preamble.tex $(FIGS)
	pandoc slides.md $(PANDOC_FLAGS) --include-in-header=notes-preamble.tex -o notes.pdf

slides-pdfpc.pdf: slides.md theme-overrides.tex pdfpc-preamble.tex $(FIGS)
	pandoc slides.md $(PANDOC_FLAGS) --include-in-header=pdfpc-preamble.tex -o slides-pdfpc.pdf

.PHONY: present present-windowed
present: slides-pdfpc.pdf
	pdfpc -n right slides-pdfpc.pdf

present-windowed: slides-pdfpc.pdf
	pdfpc -n right -w both slides-pdfpc.pdf

figs/%.png: plots/%.py plots/_common.py
	cd plots && python3 $(notdir $<) -o ../$@

.PHONY: figs clean
figs: $(FIGS)

clean:
	rm -f figs/*.png slides.pdf notes.pdf slides-pdfpc.pdf
