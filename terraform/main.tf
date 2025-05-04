module "db" {
  source      = "./modules/db"
  db_password = var.db_password
  db_name     = var.db_name
  db_user     = var.db_user
}

resource "aws_iam_role" "beanstalk_ec2_role" {
  name = "aws-elasticbeanstalk-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "beanstalk_web_tier" {
  role       = aws_iam_role.beanstalk_ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSElasticBeanstalkWebTier"
}

resource "aws_iam_instance_profile" "beanstalk_instance_profile" {
  name = "aws-elasticbeanstalk-ec2-role"
  role = aws_iam_role.beanstalk_ec2_role.name
}

resource "aws_elastic_beanstalk_application" "microservice" {
  name        = var.app_name
  description = "Aplicación Elastic Beanstalk para el microservicio"
}

resource "aws_elastic_beanstalk_environment" "microservice_env" {
  name        = "${var.app_name}-env"
  application = aws_elastic_beanstalk_application.microservice.name
  # https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.platforms.html
  # https://docs.aws.amazon.com/elasticbeanstalk/latest/platforms/platform-history-docker.html#platform-history-2025-04-24
  # https://docs.aws.amazon.com/elasticbeanstalk/latest/platforms/platform-history-python.html#platform-history-2025-04-24
  solution_stack_name = "64bit Amazon Linux 2023 v4.5.1 running Python 3.13"

  setting {
    namespace = "aws:autoscaling:asg"
    name      = "MinSize"
    value     = "3"
  }

  setting {
    namespace = "aws:autoscaling:asg"
    name      = "MaxSize"
    value     = "6"
  }

  setting {
    namespace = "aws:elasticbeanstalk:command"
    name      = "DeploymentPolicy"
    value     = var.deployment_policy
  }

  setting {
    namespace = "aws:elasticbeanstalk:environment:process:default"
    name      = "HealthCheckPath"
    value     = "/ping"
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = aws_iam_instance_profile.beanstalk_instance_profile.name
  }
}

