terraform {
  required_version = "~> 1.3"

  cloud {
    organization = "fastapi-sandbox"

    workspaces {
      name = "infrastructure"
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.47.0"
    }
  }
}
