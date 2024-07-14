import mlflow
from mlflow import MlflowClient
import time

mlflow.set_tracking_uri(uri="http://mlflow:5001")
mlflow.set_experiment("diabetes")

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def transform_custom(data, *args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here
    best_run = mlflow.search_runs(
        order_by=["metrics.f1_score DESC"],
        max_results=10,
    ).iloc[0]
    model_name = "diabetes_model"
    model_uri = f"runs:/{best_run.run_id}/model"
    model_version = mlflow.register_model(model_uri, model_name)
    # need to sleep for a moment
    time.sleep(30)

    client = MlflowClient()
    client.set_registered_model_alias(model_name, "champion", model_version.version)

    return data
