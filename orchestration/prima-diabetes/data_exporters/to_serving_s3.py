import mlflow
from mlflow import MlflowClient
import os

import boto3


uri = "http://mlflow:5002"
mlflow.set_tracking_uri(uri=uri)
mlflow.set_experiment("diabetes")

s3_client = boto3.client("s3")
s3_resource = boto3.resource("s3")

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


def list_objects(bucket_name, prefix):
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if "Contents" in response:
        return response["Contents"]
    else:
        return []


def copy_objects(source_bucket, source_prefix, destination_bucket, destination_prefix):
    objects = list_objects(source_bucket, source_prefix)
    for obj in objects:
        copy_source = {"Bucket": source_bucket, "Key": obj["Key"]}
        destination_key = destination_prefix + obj["Key"][len(source_prefix) :]
        print(f"Copying {obj['Key']} to {destination_key}")
        s3_resource.Object(destination_bucket, destination_key).copy(copy_source)


#


@data_exporter
def export_data(data, *args, **kwargs):
    """
    Function is to export model from champion to serving s3 bucket
    """
    artifact_bucket = os.getenv("S3_MLFLOW_BUCKET_NAME")
    serving_bucket = os.getenv("S3_SERVING_BUCKET")

    client = MlflowClient(tracking_uri=uri)
    logged_model = client.get_model_version_by_alias("diabetes_model", "champion")
    artifact_prefix = logged_model.source.replace(f"s3://{artifact_bucket}/", "")

    print(artifact_prefix)
    listed_objects = list_objects(artifact_bucket, artifact_prefix)
    print(listed_objects)

    # Execute the copy process
    copy_objects(artifact_bucket, artifact_prefix, serving_bucket, "champion")
