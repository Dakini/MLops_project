FROM mageai/mageai:latest

WORKDIR /app

# # Copy all files from the mage_docker directory to /app
COPY ./orchestration/mage_docker /app


# # Install dependencies
RUN pip install -r requirements.txt

#expose the code for the docker
RUN export PYTHONPATH=$PYTHONPATH:/app/project_code
