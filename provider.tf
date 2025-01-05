terraform {
  required_providers {
    external = {
      source  = "hashicorp/external"
      version = "2.3.4"
    }

    aws = {
      source  = "hashicorp/aws"
      version = "5.82.2"
    }
  }
}
