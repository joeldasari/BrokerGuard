SYSTEM_PYTHON ?= python3
VENV_PYTHON := .venv/bin/python3
PYTHON ?= $(VENV_PYTHON)
PIP ?= $(VENV_PYTHON) -m pip

.PHONY: install up-insecure up-hardened down scan scan-json test clean

install:
	$(SYSTEM_PYTHON) -m venv .venv
	$(PIP) install -r requirements.txt

up-insecure:
	cd docker && BROKER_PROFILE=insecure docker compose up -d

up-hardened:
	cd docker && BROKER_PROFILE=hardened docker compose up -d

down:
	cd docker && docker compose down

scan:
	$(PYTHON) brokerguard.py

scan-json:
	$(PYTHON) brokerguard.py --json

test:
	$(PYTHON) -m unittest discover -s tests -p "test_*.py" -v

clean:
	rm -rf .venv .pytest_cache
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -f brokerguard.log
