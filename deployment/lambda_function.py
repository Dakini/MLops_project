import os

import model

PREDICTIONS_STREAM_NAME = os.getenv("PREDICTIONS_STREAM_NAME", "diabetes-predictions")
TEST_RUN = os.getenv("TEST_RUN", "False") == "True"


model_service = model.init(
    prediction_stream_name=PREDICTIONS_STREAM_NAME,
    test_run=TEST_RUN,
)


def lambda_handler(event, context):
    return {"hello": "hello"}  # model_service.lambda_handler(event)
