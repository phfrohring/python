# Interface.
.PHONY: help test dev doc clean
.DEFAULT_GOAL := help

# Shell commands are interpreted by Bash.
SHELL := /bin/bash

# The directory in which make is executed is considered the root directory.  `root
# directory` means that all relative directories are to be interpreted relative to
# this one.
# Example: the file named `a_file` has a path: `$(set_root)/a_file`
set_root := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

# web navigator
navigator_web := brave-browser

# This makefile
this_makefile := makefile

# This setup.cfg
this_setup_cfg := setup.cfg

# Directory of sources.
set_src := src
points_src := $(shell find $(set_src) -type f -name "*.py")
$(set_src): $(points_src)
	@echo "Target: $@"
	@echo "  Newer dependencies: $?"
	@mkdir -p $@
	@touch $@

# Directory of docs.
root_doc := docs
makefile_doc := $(root_doc)/Makefile
build_doc := $(root_doc)/build
set_doc := $(root_doc)/source
points_doc := $(shell find $(set_doc) -type f)
$(set_doc): $(points_doc)
	@echo "Target: $@"
	@echo "  Newer dependencies: $?"
	@mkdir -p $@
	@touch $@

# Directory of tests.
set_test := tests
points_test := $(shell find $(set_test) -type f -name "*.py")
$(set_test): $(points_test)
	@echo "Target: $@"
	@echo "  Newer dependencies: $?"
	@mkdir -p $@
	@touch $@

# Directory of logs.
set_log := logs
test_log := $(set_log)/test.log
dev_log := $(set_log)/dev.log

# Directory of docs.
root_dist := dist

help:  ## Print help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

test: $(test_log) ## Test package.
	@echo "Target: $@"
	@cat $<

dev: $(dev_log) ## Install a the package in editable mode. 
	@echo "Target: $@"
	@cat $<

doc: $(build_doc) ## Build documentation.
	@echo "Target: $@"
	@$(navigator_web) $(build_doc)/html/index.html

publish: ## Publish to PyPi.
	@echo "Target: $@"
	@python -m build; twine upload $(root_dist)/*

clean: ## Remove built files.
	rm -rf $(set_log)/*
	rm -rf $(build_doc)/*

$(build_doc): $(makefile_doc) $(set_src) $(set_doc) $(dev_log)
	@echo "Target: $@"
	@echo "  Newer dependencies: $?"
	@cd $(root_doc); $(MAKE) html
	@touch $@

$(test_log): $(set_test) $(set_src) $(this_makefile) $(dev_log)
	@echo "Target: $@"
	@echo "  Newer dependencies: $?"
	@-pytest $< > $@

$(dev_log): $(this_setup_cfg)
	@echo "Target: $@"
	@echo "  Newer dependencies: $?"
	@-pip install -e .[dev] > $@

$(makefile_doc):
	@echo "Target: $@"
	@sphinx-quickstart --ext-autodoc --ext-intersphinx --ext-todo --ext-viewcode $(root_doc)

