resource "aws_dynamodb_table" "tf_lock_dynamodb_table" {
  name           = "${var.project}-tf-state-lock"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name    = "${var.project}-tf-state-lock"
    Project = var.project
  }
}
