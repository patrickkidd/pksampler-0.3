
clean:
	rm -rf *.pyo *.pyc *~ `find . -name "*.py~"` `find . -name "*.pyc"` pksamplerconfig.py pksamplerconfig.pyc

distclean:
	rm -rf *.pyo *.pyc *~ `find . -name "*.pyc"` `find . -name "*.pyo"` `find . -name "*.py~"` pksamplerconfig.py pksampler/pov/embedded_pixmaps.py

install:
	python install.py



