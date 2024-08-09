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
#create a ec2 instance to launch docker compose on
#expose ports and other stuff.

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
