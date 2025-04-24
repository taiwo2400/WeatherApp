output "lambda_function_name" {
  value = aws_lambda_function.fastapi_lambda.function_name
}

output "api_gateway_url" {
  value = aws_api_gatewayv2_api.fastapi_api.api_endpoint
}
