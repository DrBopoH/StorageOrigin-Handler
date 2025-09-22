VENV_DIR = .venv

mount_venv:
	if not exist $(VENV_DIR) uv venv $(VENV_DIR)

sync: mount_venv
	uv sync

run_tests:       ; uv run python -m pytest
run_vtests:      ; uv run python -m pytest -v
run_covtests:    ; uv run python -m pytest --cov=. --cov-report=html
run_vcovtests:   ; uv run python -m pytest -v --cov=. --cov-report=html


.PHONY: mount_venv sync run_tests run_vtests run_covtests run_vcovtests