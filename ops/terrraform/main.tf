provider "aws" {
  region = "us-east-1"
}


resource "aws_ecr_repository" "fastapi_lambda" {
  name = "fastapi-lambda-${var.environment}"
}

resource "aws_lambda_function" "fastapi_lambda" {
  function_name = "fastapi-lambda-${var.environment}"
  image_uri     = "${aws_ecr_repository.fastapi_lambda.repository_url}:${var.environment}"

  memory_size = 128
  timeout     = 15

  role = aws_iam_role.lambda_exec.arn
}

resource "aws_api_gatewayv2_api" "fastapi_api" {
  name          = "fastapi-api-${var.environment}"
  protocol_type = "HTTP"
}

resource "aws_iam_role" "lambda_exec" {
  name               = "lambda_exec_role-${var.environment}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}
