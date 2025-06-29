variable "key_name" {
  description = "The name of your AWS EC2 key pair"
  type        = string
}

variable "db_password" {
  description = "The database password"
  type        = string
  sensitive   = true
}
