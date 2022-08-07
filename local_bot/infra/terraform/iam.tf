resource "aws_iam_user" "local_bot_iam_user" {
  name = "${var.project}-user"

  tags = {
    name    = "local-bot-user"
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
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "dynamodb:PutItem",
          "dynamodb:DeleteItem",
          "dynamodb:GetItem",
          "dynamodb:UpdateItem"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:dynamodb:${var.region}:${var.account_id}:table/${var.dynamodb_table_name}"
      },
    ]
  })
}

resource "aws_iam_access_key" "local_bot_iam_access_key" {
  user = aws_iam_user.local_bot_iam_user.name
}

output "aws_iam_smtp_password_v4" {
  value     = aws_iam_access_key.local_bot_iam_access_key.ses_smtp_password_v4
  sensitive = true
}
