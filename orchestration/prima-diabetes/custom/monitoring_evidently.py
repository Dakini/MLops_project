from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import (
    ColumnDriftMetric,
    DatasetDriftMetric,
    DatasetMissingValuesMetric,
)

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


def create_column_mapping(
    map_columns: list = [
        "pregnancies",
        "glucose",
        "bloodpressure",
        "skinthickness",
        "insulin",
        "bmi",
        "diabetespedigreefunction",
        "age",
    ]
):
    column_mapping = ColumnMapping(
        target=None,
        prediction="pred_outcome",
        numerical_features=map_columns,
    )

    return column_mapping


def create_report():
    report = Report(
        metrics=[
            ColumnDriftMetric(column_name="pred_outcome"),
            DatasetDriftMetric(),
            DatasetMissingValuesMetric(),
        ]
    )
    return report


@custom
def transform_custom(data, *args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here
    training_data, validation_data = data
    column_mapping = create_column_mapping()
    report = create_report()

    report.run(
        reference_data=training_data,
        current_data=validation_data,
        column_mapping=column_mapping,
    )
    result = report.as_dict()

    # prediction drift
    pred_drift = result["metrics"][0]["result"]["drift_score"]
    col_drift = result["metrics"][1]["result"]["number_of_drifted_columns"]
    missing_values = result["metrics"][2]["result"]["current"][
        "share_of_missing_values"
    ]

    return pred_drift, col_drift, missing_values


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
