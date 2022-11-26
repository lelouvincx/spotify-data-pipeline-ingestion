resource "aws_s3_bucket" "de_bucket_prod" {
  bucket = "${var.bucket_name}"
  force_destroy = true
  tags = {
    Environment = "prod"
  }
}
