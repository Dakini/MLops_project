LOCAL_TAG:=$(shell date +"%Y-%m-%d-%H-%M")
LOCAL_IMAGE_NAME:=spotify-prediction:${LOCAL_TAG}

test:
	pytest tests/

quality_checks:
	black .
	flake8 .

build: quality_checks test
	docker build -t ${LOCAL_IMAGE_NAME} .

setup_mlflow: setup #build
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} mlflow-orchestration/setup.sh

destroy_mlflow:
	mlflow-orchestration/destroy.sh

setup:
	pipenv install --dev
	export PYTHONPATH=$PYTHONPATH:${pwd}/project_code
	pre-commit install
