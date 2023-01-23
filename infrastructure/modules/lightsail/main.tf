locals {
  name = "${var.env}-${var.name}"
}

resource "aws_lightsail_container_service" "default" {
  name        = local.name
  power       = var.power
  scale       = 1
  is_disabled = var.is_disabled
  tags = var.tags

  private_registry_access {
    ecr_image_puller_role {
      is_active = true
    }
  }
  depends_on = [
    aws_ecr_repository.webapp
  ]
}

resource "aws_lightsail_container_service_deployment_version" "webapp" {
  container {
    container_name = var.container_name
    image          = ":dev-psicoapp-webserver.webapp.1"

    command = []

    environment = {
      DB_HOST = aws_lightsail_database.default.master_endpoint_address
    }

    ports = {
      5000 = "HTTP"
    }
  }

  public_endpoint {
    container_name = var.container_name
    container_port = 5000

    health_check {
      healthy_threshold   = 2
      unhealthy_threshold = 2
      timeout_seconds     = 2
      interval_seconds    = 5
      path                = "/"
      success_codes       = "200-499"
    }
  }
  service_name = aws_lightsail_container_service.default.name
  depends_on = [
    aws_ecr_repository.webapp
  ]
}

resource "aws_ecr_repository_policy" "default" {
  repository = aws_ecr_repository.webapp.name

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowLightsailPull",
      "Effect": "Allow",
      "Principal": {
        "AWS": "${aws_lightsail_container_service.default.private_registry_access[0].ecr_image_puller_role[0].principal_arn}"
      },
      "Action": [
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer"
      ]
    }
  ]
}
EOF
  depends_on = [
    aws_ecr_repository.webapp
  ]
}

resource "aws_lightsail_database" "default" {
  relational_database_name  = "psicoapp"
  availability_zone         = "us-east-1a"
  master_database_name      = "webapp"
  master_password           = "aparicio1234"
  master_username           = "webapp"
  blueprint_id              = "mysql_8_0"
  bundle_id                 = "micro_1_0"
  skip_final_snapshot       = true
  depends_on = [
    aws_ecr_repository.webapp
  ]
}

resource "aws_ecr_repository" "webapp" {
  name                 = "psicoapp-webapp"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
