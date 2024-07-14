import mlflow

# setting up experiment name before the two trianing
mlflow.set_tracking_uri(uri="http://mlflow:5001")
mlflow.set_experiment("diabetes")


if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
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
    Template code for testing the output of the block.
    """
    assert len(x_train) == 537, "The output is undefined"
