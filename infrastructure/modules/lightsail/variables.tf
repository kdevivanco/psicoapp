variable "region" {
    description = "Region to deploy the VM"
    default = "us-east-1"
    type = string
}

variable "env" {
    description = "Environment to deploy the VM"
    default = "dev"
    type = string
}

variable "name" {
    description = "Name of the resource group"
    default = "myResourceGroup"
    type = string
}

variable "container_name" {
    description = "Name of the container"
    default = "hello-world"
    type = string
}

variable "image" {
    description = "ECR registry Docker image"
    default = ""
    type = string
}

variable "power" {
    description = "Power of the VM"
    default = "micro"
    type = string
}

variable "is_disabled" {
    description = "Is the VM disabled"
    default = false
    type = bool
}

variable "tags" {
    description = "Tags for the VM"
    default = {
        "environment" = "dev"
        "cost_center" = "it"
    }
    type = map(string)
}
