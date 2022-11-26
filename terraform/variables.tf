## AWS account level config: region
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-southeast-1"
}

## Key to allow connection to our EC2 instance
variable "key_name" {
  description = "EC2 key name"
  type        = string
  default     = "sde-key-prod"
}

## EC2 instance type
## https://www.amazonaws.cn/en/ec2/instance-types/
variable "instance_type" {
  description = "Instance type for EC2"
  type        = string
  default     = "t2.small"
}

## S3
variable "bucket_name" {
  default = "datalake-de-course-prod"
}

variable "acl_value" {
    default = "private"
}
