from sklearn.model_selection import train_test_split

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    splitting the data into training and valdiation data
    """
    # Specify your transformation logic here
    train, val = train_test_split(data, test_size=0.3)
    print(len(train), len(val))
    return (train, val)


@test
def test_train_len(train, val, *args) -> None:
    """
    Check the length of the train data == 537
    """
    assert len(train) == 537, "The output is not same length"


@test
def test_val_len(train, val, *args) -> None:
    """
    Check the length of the validation data == 213
    """
    assert len(val) == 231, "The output is not same length"
