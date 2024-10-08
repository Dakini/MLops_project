LOCAL_TAG:=$(shell date +"%Y-%m-%d-%H-%M")
LOCAL_IMAGE_NAME:=diabetes-predict:${LOCAL_TAG}

test:
	pytest deployment/tests/

quality_checks:
	black .
	flake8 .

build: quality_checks test

	docker build -t ${LOCAL_IMAGE_NAME} deployment/

integration_test: build
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash deployment/integration-test/run.sh


local_server: #setup #build
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} orchestration/setup.sh

destroy:
	orchestration/destroy.sh

setup:
	pipenv install --dev
	pre-commit install
