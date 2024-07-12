from sklearn.model_selection import train_test_split

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
    train, val = train_test_split(data, test_size=0.3)
    print(len(train), len(val))
    return (train, val)


@test
def test_train_len(train, val, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert len(train) == 537, "The output is not same length"


@test
def test_val_len(train, val, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert len(val) == 231, "The output is not same length"
