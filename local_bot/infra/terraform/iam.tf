resource "aws_iam_user" "local_bot_iam_user" {
  name = "${var.project}-user"

  tags = {
    name    = "${var.project}-user"
    project = var.service
  }
}

resource "aws_iam_user_policy" "local_bot_iam_user_policy" {
  name = "${aws_iam_user.local_bot_iam_user.name}-policy"
  user = aws_iam_user.local_bot_iam_user.name

  policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Action   = [
          "dynamodb:PutItem",
          "dynamodb:DeleteItem",
          "dynamodb:GetItem",
          "dynamodb:UpdateItem",
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "s3:GetObject"
        ]
        Effect   = "Allow"
        Resource = [
          "arn:aws:dynamodb:${var.region}:${var.account_id}:table/${var.dynamodb_table_name}",
          "arn:aws:s3:::local-bot-tf-state/*"
        ]
      },
    ]
  })
}
