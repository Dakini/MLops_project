LOCAL_TAG:=$(shell date +"%Y-%m-%d-%H-%M")
LOCAL_IMAGE_NAME:=diabetes-predict:${LOCAL_TAG}

test: quality_checks
	pytest tests/

quality_checks: setup
	black .
	flake8 .

# build: quality_checks test
# 	docker build -t ${LOCAL_IMAGE_NAME} .

setup_server: #setup #build
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} orchestration/setup.sh

destroy:
	orchestration/destroy.sh

setup:
	pipenv install --dev
	export PYTHONPATH=$PYTHONPATH:${pwd}/project_code
	pre-commit install
