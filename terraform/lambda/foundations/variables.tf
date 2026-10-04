variable "app_name" {
  description = "Application Name"
  type        = string
  default     = "jstenghele-fastapi-sandbox"
}

variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "sa-east-1"
}

variable "github_repo" {
  description = "GitHub repository in the format owner/repo"
  type        = string
  default     = "JuanStenghele/fastapi-sandbox"
}

variable "main_domain_name" {
  description = "Main domain name"
  type        = string
  default     = "25101999.xyz"
}
