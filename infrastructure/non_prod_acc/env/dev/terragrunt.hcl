include {
  path = find_in_parent_folders()
}

terraform {
  source = "../../../modules//lightsail"
}
locals {
  env = "dev"
}

inputs = {
  name           = "psicoapp-webserver"
  env            = local.env
  power          = "micro"
  is_disabled    = false
  container_name = "webapp"
  image          = "567181624088.dkr.ecr.us-east-1.amazonaws.com/psicoapp-webapp:latest"
  tags = {
    Environment   = local.env
    ProvisionedBy = "Terraform"
  }
}