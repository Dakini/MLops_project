import mlflow


import xgboost as xgb
from sklearn.metrics import f1_score
from hyperopt import fmin, tpe, hp, Trials, STATUS_OK
from hyperopt.pyll import scope


if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


mlflow.set_tracking_uri(uri="http://mlflow:5001")
mlflow.set_experiment("diabetes")


@custom
def transform_custom(data, *args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here
    x_train, y_train, x_val, y_val = data
    train = xgb.DMatrix(x_train, label=y_train)
    valid = xgb.DMatrix(x_val, label=y_val)

    def objective(params):
        with mlflow.start_run():
            mlflow.autolog()
            booster = xgb.train(
                params=params,
                dtrain=train,
                num_boost_round=1000,
                evals=[(valid, "validation")],
                early_stopping_rounds=50,
            )
            y_pred_prob = booster.predict(valid)
            y_pred = (y_pred_prob > 0.5).astype(int)
            fscore = f1_score(y_val, y_pred)
            mlflow.log_metric("f1_score", fscore)

        return {"loss": -fscore, "status": STATUS_OK}

    search_space = {
        "max_depth": scope.int(hp.quniform("max_depth", 4, 100, 1)),
        "learning_rate": hp.loguniform("learning_rate", -3, 0),
        "reg_alpha": hp.loguniform("reg_alpha", -5, -1),
        "reg_lambda": hp.loguniform("reg_lambda", -6, -1),
        "min_child_weight": hp.loguniform("min_child_weight", -1, 3),
        "objective": "reg:linear",
        "seed": 42,
    }

    fmin(
        fn=objective,
        space=search_space,
        algo=tpe.suggest,
        max_evals=10,
        trials=Trials(),
        verbose=False,
    )

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
