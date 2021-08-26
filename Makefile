TEST_CMD  = py.test
PY_CMD    = python
PROJ_NAME = nhentai_spider

init:
	pip install -r requirements.txt

test:
	${TEST_CMD}

testv:
	${TEST_CMD} -vv

cov:
	${TEST_CMD} --cov=${PROJ_NAME}

run:
	${PY_CMD} -m ${PROJ_NAME}
