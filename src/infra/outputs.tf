output "ec2_public_ip" {
  value = aws_instance.django.public_ip
  description = "Public IP of the Django server"
}

output "rds_endpoint" {
  value = aws_db_instance.postgres.endpoint
  description = "PostgreSQL database endpoint"
}
