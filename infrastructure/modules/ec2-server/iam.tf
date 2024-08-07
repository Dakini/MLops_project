resource "aws_iam_role" "mlflow-role" {
  name = "mlflow-demo-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
      },
    ],
  })
}

resource "aws_iam_policy" "mlflow_artifact_policy" {
    name="mlflow-s3-policy"
    policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:GetObject*",
          "s3:ListBucket",
          "s3:PutObject",
          "s3:DeleteObject"
        ],
        Effect   = "Allow",
        Resource = [
          "${var.bucket-arn}",
          "${var.bucket-arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "s3_policy_attachment" {
    role = aws_iam_role.mlflow-role.id
    policy_arn = aws_iam_policy.mlflow_artifact_policy.arn
    depends_on = [ aws_iam_policy.mlflow_artifact_policy ]
}

resource "aws_iam_instance_profile" "mlflow-instance-profile" {
  name = "${var.project_id}-mlflow-ec2-instance-role"
  role = aws_iam_role.mlflow-role.name
}
