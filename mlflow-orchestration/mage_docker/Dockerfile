FROM mageai/mageai:latest

ARG USER_CODE_PATH=/home/src/${PROJECT_NAME}


RUN find . -type d -print
COPY requirements.txt ${USER_CODE_PATH}/requirements.txt
RUN pip install -r ${USER_CODE_PATH}/requirements.txt
