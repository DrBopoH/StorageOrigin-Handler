PYTHON = python
VENV_DIR = venv



VENV_PYTHON = $(VENV_DIR)\\Scripts\\python.exe
VENV_ACTIVATE = $(VENV_DIR)\\Scripts\\activate.bat

PIP = $(VENV_PYTHON) -m pip



mount_venv:
	if not exist $(VENV_DIR) $(PYTHON) -m venv $(VENV_DIR)

uptodate: mount_venv
	@cmd /c "$(VENV_ACTIVATE) & $(PIP) install -r requirements.txt"


#run_app:
#	@cmd /c "$(VENV_ACTIVATE) & $(VENV_PYTHON) main/main.py"


run_tests:
	@cmd /c "$(VENV_ACTIVATE) & $(VENV_PYTHON) -m pytest"

run_vtests:
	@cmd /c "$(VENV_ACTIVATE) & $(VENV_PYTHON) -m pytest -v"

run_covtests:
	@cmd /c "$(VENV_ACTIVATE) & $(VENV_PYTHON) -m pytest --cov=. --cov-report=html"

run_vcovtests:
	@cmd /c "$(VENV_ACTIVATE) & $(VENV_PYTHON) -m pytest -v --cov=. --cov-report=html"



clean_cache:
	del /s /q __pycache__ .pytest_cache htmlcov .coverage 2>nul || exit 0



.PHONY: mount_venv uptodate run_tests run_vtests run_covtests run_vcovtests clean_cache