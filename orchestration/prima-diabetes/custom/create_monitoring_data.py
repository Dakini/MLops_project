import mlflow
from mlflow import MlflowClient
import pandas as pd

uri = "http://mlflow:5002"
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
    Create monitoring data including traind and validation predictions
    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here
    x_train, y_train, x_val, y_val = data
    client = MlflowClient(tracking_uri=uri)
    logged_model = client.get_model_version_by_alias("diabetes_model", "champion")
    print(logged_model)
    model = mlflow.pyfunc.load_model(logged_model.source)
    train_preds = model.predict(x_train)
    train_preds = (train_preds > 0.5).astype(int)
    train_data = combine_data(x_train, y_train, train_preds)

    validation_preds = model.predict(x_val)
    validation_preds = (validation_preds > 0.5).astype(int)
    validation_data = combine_data(x_val, y_val, validation_preds)

    return train_data, validation_data


@test
def test_train_len(train_data, validation_data, *args) -> None:
    """
    Check the length of the train data == 537
    """
    assert len(train_data) == 537, "The output is not same length"


@test
def test_val_len(train_data, validation_data, *args) -> None:
    """
    Check the length of the validation data == 213
    """
    assert len(validation_data) == 231, "The output is not same length"
