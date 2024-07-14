import mlflow
from mlflow import MlflowClient
import pandas as pd

uri = "http://mlflow:5001"
mlflow.set_tracking_uri(uri=uri)
mlflow.set_experiment("diabetes")

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


def combine_data(data: pd.DataFrame, outcome: list[int], pred_outcomes: list[int]):
    data["outcome"] = outcome
    data["pred_outcome"] = pred_outcomes
    data["index"] = [i for i in range(len(data))]
    return data


@custom
def transform_custom(data, *args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here
    x_train, y_train, x_val, y_val = data
    client = MlflowClient(tracking_uri=uri)
    logged_model = client.get_model_version_by_alias("diabetes_model", "champion")

    model = mlflow.pyfunc.load_model(logged_model.source)
    train_preds = model.predict(x_train)
    train_preds = (train_preds > 0.5).astype(int)
    train_data = combine_data(x_train, y_train, train_preds)

    validation_preds = model.predict(x_val)
    validation_preds = (validation_preds > 0.5).astype(int)
    validation_data = combine_data(x_val, y_val, validation_preds)

    return train_data, validation_data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
