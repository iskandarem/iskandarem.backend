terraform {
  backend "s3" {
    bucket         = "iskandarem-terraform-state"
    key            = "dev/terraform.tfstate"
    region         = "eu-north-1"
    encrypt        = true
  }
}
