terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.60.0"
    }
  }
  backend "s3" {
    bucket = "tf-state-bucket-3"
    key    = "ec2-vpc-docker.tfstate"
    region = "eu-west-2"

  }
}

provider "aws" {
  # Configuration options
  region = var.aws_region
}

data "aws_caller_identity" "current_identity" {

}
locals {
  account_id = data.aws_caller_identity.current_identity.account_id
}

#kinesis streams
module "input_stream" {
  source           = "./modules/kinesis"
  stream_name      = "${var.source_stream_name}-${var.project_id}"
  retention_period = 48
  shard_count      = 2
  tags             = var.project_id
}

#kinesis streams
module "output_stream" {
  source           = "./modules/kinesis"
  stream_name      = "${var.output_stream_name}-${var.project_id}"
  retention_period = 48
  shard_count      = 2
  tags             = var.project_id
}
#create a s3 bucket
module "mlflow-bucket" {
  source        = "./modules/s3"
  project-id    = var.project_id
  mlflow-bucket = var.mlflow-bucket-name
}

#create a serving bucket
module "serving-bucket" {
  source        = "./modules/s3"
  project-id    = var.project_id
  mlflow-bucket = var.serving-bucket-name
}


module "ecr_image" {
  depends_on                 = [module.serving-bucket]
  source                     = "./modules/ecr"
  ecr_repo_name              = "${var.ecr_repo_name}-${var.project_id}"
  account_id                 = local.account_id
  lambda_function_local_path = var.lambda_function_local_path
  docker_image_local_path    = var.docker_image_local_path
  serving_bucket             = module.serving-bucket.bucket-name

}

module "prediction_lambda" {
  source = "./modules/lambda"
  image_uri = module.ecr_image.image_uri
  source_stream_name = "${var.source_stream_name}-${var.project_id}"
  source_stream_arn = module.input_stream.stream_arn
  output_stream_name = "${var.output_stream_name}-${var.project_id}"
  output_stream_arn = module.output_stream.stream_arn
  model_bucket = module.serving-bucket.bucket-name
  lambda_function_name = "${var.lambda_function_name}_${var.project_id}"

}
# #create a ec2 instance to launch docker compose on
# #expose ports and other stuff.

module "mlflow-server" {
  source = "./modules/ec2-server"
  project_id = var.project_id
  shh-key-name = var.ssh-key-name
  depends_on = [ module.mlflow-bucket, module.serving-bucket]
  artifact-bucket-arn = module.mlflow-bucket.bucket-arn
  artifact-bucket-name = module.mlflow-bucket.bucket-name

  serving-bucket-arn = module.serving-bucket.bucket-arn
  serving-bucket-name = module.serving-bucket.bucket-name

  db_password = var.db_password
  db_name = var.db_name
  db_username = var.db_username
}

#provide a way to ssh in but also the DNS to go to the services, such as Grafana or that.

output "mlflow-server-ip" {
  value = module.mlflow-server.ip
}
output "mlflow-server-dns" {
  value = module.mlflow-server.dns
}

output "lambda_function" {
  value     = "${var.lambda_function_name}_${var.project_id}"
}

output "predictions_source_stream_name" {
  value     = "${var.source_stream_name}-${var.project_id}"
}
output "predictions_output_stream_name" {
  value     = "${var.output_stream_name}-${var.project_id}"
}
output "ecr_repo" {
  value = "${var.ecr_repo_name}_${var.project_id}"
}
