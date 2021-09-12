
terraform {
    required_providers {
        aws = {
            source="hashicorp/aws"
            version="3.55.0"
        }
    }
}

provider "aws" {
    region = "${var.aws_region}"
    shared_credentials_file = "~/.aws/credentials"
} 

variable "aws_region" {
  description = "The AWS region to create into"
  default     = "us-east-1"
}

output "lambda" {
  value = "${aws_lambda_function.lambda.qualified_arn}"
}
provider "archive" {}

data "archive_file" "zip" {
  type        = "zip"
  source_file = "botHelper.py"
  output_path = "NBA_Alert.zip"
}

data "aws_iam_policy_document" "policy" {
  statement {
    sid    = ""
    effect = "Allow"

    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = "${data.aws_iam_policy_document.policy.json}"
}

// Here creates function
resource "aws_lambda_function" "lambda" {
  function_name = "NBA_Alert_lambda"

  filename         = "${data.archive_file.zip.output_path}"
  source_code_hash = "${data.archive_file.zip.output_base64sha256}"

  role    = "${aws_iam_role.iam_for_lambda.arn}"
  handler = "botHelper.main"
  runtime = "python3.9"

}
