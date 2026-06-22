terraform {
  backend "s3" {
    bucket         = "glunk-works-tofu-state-00042"
    key            = "tri-loop-dev/terraform.tfstate" # Must be unique per project!
    region         = "us-east-1"
    dynamodb_table = "global-tofu-lock"
    encrypt        = true
  }
}