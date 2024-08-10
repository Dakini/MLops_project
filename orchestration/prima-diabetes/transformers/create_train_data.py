import mlflow

# setting up experiment name before the two trianing
mlflow.set_tracking_uri(uri="http://mlflow:5002")
mlflow.set_experiment("diabetes")


if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Creatin the X,y data for train and validation
    """
    # Specify your transformation logic here
    train, val = data

    label = "outcome"
    # create train and test datasets
    x_train = train.drop(label, axis=1)
    y_train = train[label]

    x_val = val.drop(label, axis=1)
    y_val = val[label]
    return x_train, y_train, x_val, y_val


@test
def test_output(x_train, y_train, x_val, y_val, *args) -> None:
    """
    checking that the train_data is the same length
    """
    assert len(x_train) == 537, "The output is undefined"
