resource "aws_s3_bucket" "project_spotify_bucket" {
  bucket = "${var.bucket_name}"
  force_destroy = true
  tags = {
    Environment = "prod"
  }
}
