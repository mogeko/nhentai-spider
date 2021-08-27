.PHONY: clean-pyc clean-build clean-cov clean

TEST_CMD  = py.test
PY_CMD    = python
PROJ_NAME = nhentai_spider
TEST_DIR  = tests/
SETUP     = setup.py

help:
	@echo "Usage: make [options] [target] ..."
	@echo "Target:"
	@echo "   init         nitialize the development environment."
	@echo "   test         Run the test file (by pytest)."
	@echo "   testv        Run the test file with verbose mode (by pytest)."
	@echo "   cov          Calculate code coverage (by pytest-cov)."
	@echo "   run          Run nhentai_spdier."
	@echo "   build        Package nhentai_spdier."
	@echo "   clean        Clean up this project folder."

init:
	pip install -r requirements.txt
	pip install -e .

test: ${TEST_DIR} ${PROJ_NAME}
	${TEST_CMD} ${TEST_DIR}

testv: ${TEST_DIR} ${PROJ_NAME}
	${TEST_CMD} -vv ${TEST_DIR}

cov: ${TEST_DIR} ${PROJ_NAME}
	${TEST_CMD} --cov=${PROJ_NAME} ${TEST_DIR}

cov-xml: ${TEST_DIR} ${PROJ_NAME}
	${TEST_CMD} --cov-report xml --cov=${PROJ_NAME} ${TEST_DIR}

run: ${PROJ_NAME}
	${PY_CMD} -m ${PROJ_NAME}

build: ${SETUP}
	${PY_CMD} ${SETUP} sdist

clean-pyc:
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -type d | xargs rm -fr
	@find . -name '.pytest_cache' -type d | xargs rm -fr

clean-build:
	@rm --force --recursive build/
	@rm --force --recursive dist/
	@rm --force --recursive *.egg-info

clean-cov:
	@rm --force --recursive .coverage
	@rm --force --recursive coverage.xml

clean: clean-pyc clean-build clean-cov
	@echo "## Clean all data."
