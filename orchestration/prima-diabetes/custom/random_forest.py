from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

import mlflow


mlflow.set_tracking_uri(uri="http://mlflow:5001")
mlflow.set_experiment("diabetes")
# mlflow.set_tracking_uri(uri=f"http://{host}:5001")
# print(experiment_name)
if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(data, *args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here
    x_train, y_train, x_val, y_val = data
    with mlflow.start_run():
        pipeline = make_pipeline(
            StandardScaler().fit(x_train), RandomForestClassifier(n_jobs=-1)
        )

        pipeline.fit(x_train, y_train)
        y_pred = pipeline.predict(x_val)

        fscore = f1_score(y_pred, y_val)
        print(fscore)
        mlflow.log_metric("f1_score", fscore)

        mlflow.sklearn.log_model(pipeline, artifact_path="model")
    return {}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """

    assert output is not None, "The output is undefined"


# @test
# def test_model_is_there(output, *args, **kwargs):
#     x, y = output
#     logged_model = 'runs:/a813b7ec59f842eda63ae828867ce266/model'

#     # Load model as a PyFuncModel.
#     loaded_model = mlflow.pyfunc.load_model(logged_model)

#     pred = model.predict([x])
#     print(pred, 'far far far ')
