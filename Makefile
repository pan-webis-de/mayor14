# Makefile for homepage


doc: README
	rst2html -s README > README.html

.PHONY: clean
clean:
	rm -rf $(DEPLOY_DIR)


