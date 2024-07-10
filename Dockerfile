FROM python:3.10-slim
RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app
COPY ["Pipfile", "Pipfile.lock", "./"]
COPY ["project_code/",  "./"]
COPY ["tests/",  "./"]
RUN pipenv install --system --deploy
RUN export PYTHONPATH=$PYTHONPATH:/app/project_code
# RUN ls
# RUN pipenv run pytest tests
RUN bash -c "ls"

ENTRYPOINT [ "bash" ]
