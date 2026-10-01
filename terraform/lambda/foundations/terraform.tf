terraform {
  required_version = "~> 1.15"

  cloud {
    organization = "fastapi-sandbox"

    workspaces {
      name = "lambda-foundations"
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.47"
    }
  }
}
