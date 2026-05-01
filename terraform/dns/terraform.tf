terraform {
  required_version = "~> 1.3"

  cloud {
    organization = "fastapi-sandbox"

    workspaces {
      name = "dns"
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.47.0"
    }

    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.20"
    }
  }
}
