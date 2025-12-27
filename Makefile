# Makefile for patterntest

PREFIX ?= /usr
DESTDIR ?=
PYTHON ?= python3
INSTALL ?= install

# Installation directories
BINDIR = $(DESTDIR)$(PREFIX)/bin
LIBDIR = $(DESTDIR)$(PREFIX)/lib/$(PYTHON)/dist-packages
SHAREDIR = $(DESTDIR)$(PREFIX)/share/patterntest
DOCDIR = $(DESTDIR)$(PREFIX)/share/doc/patterntest

# Source files
BINARIES = patterntest dirunpack
PYTHON_LIB = ptlib logger.py

.PHONY: all install install-debug clean

all:
	@echo "patterntest - no build required"

install: all
	# Install binaries
	$(INSTALL) -d $(BINDIR)
	$(INSTALL) -m 755 $(BINARIES) $(BINDIR)/
	
	# Install Python library
	$(INSTALL) -d $(LIBDIR)
	$(INSTALL) -d $(LIBDIR)/ptlib
	$(INSTALL) -d $(LIBDIR)/ptlib/formats
	$(INSTALL) -d $(LIBDIR)/ptlib/modes
	$(INSTALL) -d $(LIBDIR)/ptlib/patterns
	$(INSTALL) -m 644 logger.py $(LIBDIR)/
	$(INSTALL) -m 644 ptlib/*.py $(LIBDIR)/ptlib/
	$(INSTALL) -m 644 ptlib/formats/*.py $(LIBDIR)/ptlib/formats/
	$(INSTALL) -m 644 ptlib/modes/*.py $(LIBDIR)/ptlib/modes/
	$(INSTALL) -m 644 ptlib/patterns/*.py $(LIBDIR)/ptlib/patterns/
	
	# Install data files
	$(INSTALL) -d $(SHAREDIR)
	$(INSTALL) -m 644 example.dir $(SHAREDIR)/
	
	# Install documentation
	$(INSTALL) -d $(DOCDIR)
	$(INSTALL) -m 644 README.md $(DOCDIR)/
	$(INSTALL) -m 644 LOGGING.md $(DOCDIR)/
	$(INSTALL) -m 644 Console-Dev.md $(DOCDIR)/
	
	# Install AppData
	$(INSTALL) -d $(DESTDIR)$(PREFIX)/share/metainfo
	$(INSTALL) -m 644 debian/patterntest.appdata.xml $(DESTDIR)$(PREFIX)/share/metainfo/
	
	@echo "Installation complete to $(DESTDIR)$(PREFIX)"

install-debug: all
	# Create symlinks in /usr pointing to project directory
	# Note: Does NOT respect DESTDIR/PREFIX
	@if [ "$$(id -u)" -ne 0 ]; then \
		echo "Error: install-debug requires root privileges"; \
		exit 1; \
	fi
	@PROJECT_DIR=$$(pwd); \
	$(INSTALL) -d /usr/bin && \
	ln -sf $$PROJECT_DIR/patterntest /usr/bin/patterntest && \
	ln -sf $$PROJECT_DIR/dirunpack /usr/bin/dirunpack && \
	$(INSTALL) -d /usr/lib/$(PYTHON)/dist-packages && \
	ln -sf $$PROJECT_DIR/logger.py /usr/lib/$(PYTHON)/dist-packages/logger.py && \
	ln -sf $$PROJECT_DIR/ptlib /usr/lib/$(PYTHON)/dist-packages/ptlib && \
	$(INSTALL) -d /usr/share/patterntest && \
	ln -sf $$PROJECT_DIR/example.dir /usr/share/patterntest/example.dir && \
	$(INSTALL) -d /usr/share/doc/patterntest && \
	ln -sf $$PROJECT_DIR/README.md /usr/share/doc/patterntest/README.md && \
	ln -sf $$PROJECT_DIR/LOGGING.md /usr/share/doc/patterntest/LOGGING.md && \
	ln -sf $$PROJECT_DIR/Console-Dev.md /usr/share/doc/patterntest/Console-Dev.md && \
	ln -sf $$PROJECT_DIR/debian/patterntest.appdata.xml /usr/share/metainfo/patterntest.appdata.xml && \
	echo "Debug installation complete (symlinks in /usr)"

clean:
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -f *.html *.pdf *.tex *.csv *.md *.txt 2>/dev/null || true
	@echo "Clean complete"

uninstall:
	rm -f $(BINDIR)/patterntest $(BINDIR)/dirunpack
	rm -rf $(LIBDIR)/ptlib $(LIBDIR)/logger.py
	rm -rf $(SHAREDIR)
	rm -rf $(DOCDIR)
	rm -f $(DESTDIR)$(PREFIX)/share/metainfo/patterntest.appdata.xml
	@echo "Uninstall complete"

uninstall-debug:
	@if [ "$$(id -u)" -ne 0 ]; then \
		echo "Error: uninstall-debug requires root privileges"; \
		exit 1; \
	fi
	rm -f /usr/bin/patterntest /usr/bin/dirunpack
	rm -f /usr/lib/$(PYTHON)/dist-packages/logger.py
	rm -f /usr/lib/$(PYTHON)/dist-packages/ptlib
	rm -f /usr/share/patterntest/example.dir
	rm -f /usr/share/doc/patterntest/README.md
	rm -f /usr/share/doc/patterntest/LOGGING.md
	rm -f /usr/share/doc/patterntest/Console-Dev.md
	rm -f /usr/share/metainfo/patterntest.appdata.xml
	@echo "Debug uninstall complete"

