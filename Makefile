# Intent — one-command bootstrap + test.
# `make setup` builds the only venv that needs third-party deps (servers/).
# `make test` runs every suite through it. Everything else is stdlib.

PY    ?= python3
VENV  := servers/.venv
VPY   := $(CURDIR)/$(VENV)/bin/python

# NOTE: this repo is a slice of a larger Workspaces monorepo. The cross-product
# value-term *invariant* suites (test_value_term_invariants.py,
# test_retired_term_invariants.py) scan from /home for sibling products
# (cast, forge, loom, voices, …) that only exist in the full monorepo, so they
# fail by design in a standalone clone. `make test` runs the repo-local suites;
# `make test-invariants` runs the monorepo suite (green only inside Workspaces).

.PHONY: help setup test test-servers test-tools test-root test-invariants clean

INVARIANT_SUITES := test_value_term_invariants.py test_retired_term_invariants.py

help: ## Show this help
	@grep -hE '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
	  | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

setup: $(VENV) ## Create servers venv + install deps (fastmcp, pyyaml, pytest)

$(VENV):
	$(PY) -m venv $(VENV)
	$(VENV)/bin/pip install -q --upgrade pip
	$(VENV)/bin/pip install -q -r servers/requirements.txt

test: setup test-servers test-tools test-root ## Run repo-local suites (110 tests, all green)

test-servers: setup ## Knowledge/coherence engine + MCP servers (needs venv)
	cd servers && $(VPY) -m pytest -q

test-tools: setup ## flight-model + value-term-audit (stdlib)
	cd tools && $(VPY) -m pytest -q $(addprefix --ignore=,$(INVARIANT_SUITES))

test-root: setup ## engagement-isolation + repo-level tests (stdlib)
	$(VPY) -m pytest tests -q

test-invariants: setup ## Cross-product value-term invariants — REQUIRES full Workspaces monorepo
	cd tools && $(VPY) -m pytest -q $(INVARIANT_SUITES)

clean: ## Remove venv + caches
	rm -rf $(VENV)
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
