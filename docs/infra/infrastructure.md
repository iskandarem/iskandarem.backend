# Infrastructure Documentation

## What is Terraform?

Terraform is a tool that helps you create and manage your infrastructure using code. Instead of clicking around in the AWS console or other cloud providers, you write simple configuration files that describe what resources you want (like servers, databases, or networks). Terraform then takes care of creating, updating, or deleting these resources for you automatically.

Using Terraform means your infrastructure setup is easy to reproduce, track changes, and share with others.

---

## Infrastructure Setup

This project uses Terraform to build an AWS infrastructure with the following:

- An ECR repository to store Docker images
- An ECS cluster and service running tasks on Fargate
- Load balancer and target group for handling incoming traffic
- Security groups for controlling network access
- IAM roles for permissions
- Use of default VPC and subnets
- Remote Terraform state stored in an existing S3 bucket

---

### Terraform State

We keep track of Terraform's state remotely in an existing S3 bucket to share state between runs.

```hcl
data "aws_s3_bucket" "terraform_state" {
  bucket = "iskandarem-terraform-state"
}
```
### Provider Configuration

Here we set the AWS provider and specify the region.
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.45.0"
    }
  }
}

provider "aws" {
  region = var.region
}
```

### ECR Repository

Creates a container registry for storing Docker images.
```hcl
resource "aws_ecr_repository" "iskandarem_ecr_repo" {
  name = "iskandarem"
}
```

### ECS Cluster and Task Definition

Create a cluster and define how the container should run.
```hcl
resource "aws_ecs_cluster" "iskandarem_cluster" {
  name = "iskandarem-cluster"
}

resource "aws_ecs_task_definition" "iskandarem_task" {
  family                   = "iskandarem-first-task"
  container_definitions    = <<DEFINITION
  [
    {
      "name": "iskandarem-first-task",
      "image": "${aws_ecr_repository.iskandarem_ecr_repo.repository_url}:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "hostPort": 8000
        }
      ],
      "memory": 512,
      "cpu": 256
    }
  ]
  DEFINITION
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  memory                   = 512
  cpu                      = 256
  execution_role_arn       = "${aws_iam_role.ecsTaskExecutionRole.arn}"
}
```

### IAM Role

Gives ECS tasks permission to interact with AWS services.
```hcl

resource "aws_iam_role" "ecsTaskExecutionRole" {
  name               = "ecsTaskExecutionRole"
  assume_role_policy = "${data.aws_iam_policy_document.assume_role_policy.json}"
}

data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
  role       = "${aws_iam_role.ecsTaskExecutionRole.name}"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}
```


### VPC and Subnets

Use AWS default VPC and subnets.

```hcl

resource "aws_default_vpc" "default_vpc" {}

resource "aws_default_subnet" "default_subnet_a" {
  availability_zone = "eu-north-1a"
}

resource "aws_default_subnet" "default_subnet_b" {
  availability_zone = "eu-north-1b"
}
```

### Load Balancer and Security Groups

Set up the Application Load Balancer and security groups.

```hcl
resource "aws_alb" "application_load_balancer" {
  name               = "load-balancer-dev"
  load_balancer_type = "application"
  subnets            = [
    aws_default_subnet.default_subnet_a.id,
    aws_default_subnet.default_subnet_b.id
  ]
  security_groups    = [aws_security_group.load_balancer_security_group.id]
}

resource "aws_security_group" "load_balancer_security_group" {
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "service_security_group" {
  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.load_balancer_security_group.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### Target Group and Listener

Forward requests from the load balancer to the ECS service.

```hcl
resource "aws_lb_target_group" "target_group" {
  name        = "target-group"
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_default_vpc.default_vpc.id
}

resource "aws_lb_listener" "listener" {
  load_balancer_arn = aws_alb.application_load_balancer.arn
  port              = "80"
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.target_group.arn
  }
}
```

### ECS Service

Runs and manages the container instances.
```hcl
resource "aws_ecs_service" "iskandarem_service" {
  name            = "iskandarem-first-service"
  cluster         = aws_ecs_cluster.iskandarem_cluster.id
  task_definition = aws_ecs_task_definition.iskandarem_task.arn
  launch_type     = "FARGATE"
  desired_count   = 3

  load_balancer {
    target_group_arn = aws_lb_target_group.target_group.arn
    container_name   = aws_ecs_task_definition.iskandarem_task.family
    container_port   = 8000
  }

  network_configuration {
    subnets          = [
      aws_default_subnet.default_subnet_a.id,
      aws_default_subnet.default_subnet_b.id
    ]
    assign_public_ip = true
    security_groups  = [aws_security_group.service_security_group.id]
  }
}

```
