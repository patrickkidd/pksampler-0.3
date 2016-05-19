
all:
	@echo "Rendering images"
	python make.py --all 2> /dev/null
	@echo "Applying masks to and embedding pixmaps into \"../embedded_pixmaps.py\""
	@python mask.py
