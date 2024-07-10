import numpy as np
from sklearn.linear_model import LogisticRegression

import mlflow
import mlflow.sklearn

host = "0.0.0.0"
mlflow.set_tracking_uri(f"http://{host}:5001")
mlflow.set_experiment("asdasd")


def train():
    with mlflow.start_run():
        mlflow.sklearn.autolog()
        X = np.array([-2, -1, 0, 1, 2, 1]).reshape(-1, 1)
        y = np.array([0, 0, 1, 1, 1, 0])

        lr = LogisticRegression()
        lr.fit(X, y)
        score = lr.score(X, y)
        mlflow.log_metric("score", score)


if __name__ == "__main__":
    train()
