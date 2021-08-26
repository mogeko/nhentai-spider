TEST_CMD  = py.test
PY_CMD    = python
PROJ_NAME = nhentai_spider
TEST_DIR  = tests/

init:
	pip install -r requirements.txt

test:
	${TEST_CMD} ${TEST_DIR}

testv:
	${TEST_CMD} -vv ${TEST_DIR}

cov:
	${TEST_CMD} --cov=${PROJ_NAME} ${TEST_DIR}

run:
	${PY_CMD} -m ${PROJ_NAME}
