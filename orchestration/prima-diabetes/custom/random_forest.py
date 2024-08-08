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

        mlflow.log_metric("f1_score", fscore)

        mlflow.sklearn.log_model(pipeline, artifact_path="model")
    return {}





