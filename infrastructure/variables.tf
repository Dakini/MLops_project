variable "aws_region" {
  description = "aws region"
}

variable "project_id" {
  description = "project-id"
}
variable "mlflow-bucket-name" {
  description = "name of the s3 bucket"
}

variable "serving-bucket-name" {
  description = "name of the s3 serving bucket"
}

variable "db_name" {
  description = "name of the rds database"
}
variable "db_username" {
  description = "postgress user name"
}

variable "source_stream_name" {
  description = "name of the source kinesis stream"
}

variable "output_stream_name" {
  description = "name of the source kinesis stream"
}
variable "db_password" {
  description = "postgress password"
}

variable "ssh-key-name" {
  description = "name of the ssh key for the ec2 instance"
}

variable "lambda_function_local_path" {
  description = ""
}

variable "docker_image_local_path" {
  description = ""
}

variable "ecr_repo_name" {
  description = ""
}

variable "lambda_function_name" {
  description = ""
}
