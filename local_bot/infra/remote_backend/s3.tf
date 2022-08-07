resource "aws_s3_bucket" "tf_state_s3_bucket" {
  bucket        = "${var.project}-tf-state"
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "tf_state_s3_bucket_versioning" {
  bucket = aws_s3_bucket.tf_state_s3_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "tf_state_s3_bucket_sse_configuration" {
  bucket = aws_s3_bucket.tf_state_s3_bucket.bucket
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
