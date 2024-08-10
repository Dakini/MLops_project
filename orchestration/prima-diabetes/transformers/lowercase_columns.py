if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    trasform columns into lower column data
    """
    # Specify your transformation logic here
    data.columns = [c.lower().replace(" ", "_") for c in data.columns]
    return data


@test
def test_cols_lower(output, *args):
    """Test if the Age column is lower case"""
    assert "age" in output.columns
