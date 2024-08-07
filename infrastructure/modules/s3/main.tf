
resource "aws_s3_bucket" "mlflow-bucket" {
  bucket = "${var.project-id}-${var.mlflow-bucket}"
  acl = "private"
  force_destroy = true

  tags = {
    Name        = "${var.project-id}-${var.mlflow-bucket}"
    Environment = "Dev"
  }
}

output "bucket-name" {
  value = aws_s3_bucket.mlflow-bucket.bucket
}
output "bucket-arn" {
  value = aws_s3_bucket.mlflow-bucket.arn
}
