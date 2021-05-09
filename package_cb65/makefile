# Interface.
.PHONY: help publish clean
.DEFAULT_GOAL := help

# Shell commands are interpreted by Bash.
SHELL := /bin/bash

# The directory in which make is executed is considered the root directory.  `root
# directory` means that all relative directories are to be interpreted relative to
# this one.
# Example: the file named `a_file` has a path: `$(set_root)/a_file`
set_root := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

# This makefile
this_makefile := makefile

# Directory of docs.
root_dist := dist

help:  ## Print help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

publish: ## Publish to PyPi.
	@echo "Target: $@"
	@python -m build; twine upload $(root_dist)/*

clean: ## Remove built files.
	rm -rf $(root_dist)/*

