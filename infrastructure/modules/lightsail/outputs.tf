# output name {
#   value       = aws_lightsail_container_service.default.private_registry_access[0].ecr_image_puller_role[0].principal_arn
#   sensitive   = false
#   description = "description"
#   depends_on  = []
# }

output "db_endpoint" {
  value       = aws_lightsail_database.default.master_endpoint_address 
  sensitive   = false
  description = "the DB endpoint"
  depends_on  = []
}

output "db_port" {
  value       = aws_lightsail_database.default.master_endpoint_port 
  sensitive   = false
  description = "the DB port"
  depends_on  = []
}