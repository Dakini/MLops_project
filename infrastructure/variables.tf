

variable "aws_region" {
  description = "aws region"
  default     = "eu-west-2"
}

variable "project_id" {
  description = "project-id"
  default     = "prima-diabetes"
}
variable "mlflow-bucket-name" {
  description = "name of the s3 bucket"
  default     = "mlflow-model-3-bucket"

}
variable "db_name" {
  description = "name of the rds database"
  default     = "projectDb"
}
variable "db_username" {
  description = "postgress user name"
  default     = "postgresS"
}

variable "db_password" {
  description = "postgress password"
  default     = "passw0rd"
}

variable "ssh-key-name" {
  description = "name of the ssh key for the ec2 instance"
  default     = "ssh-key"
}
