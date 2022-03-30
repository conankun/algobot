variable "zip_file_name" {
  description = "The name of the zip file that contains code to run."
  type = string
}

variable "discord_bot_token" {
  description = "Token of the discord bot."
  type = string
}

variable aws_access_key_id {
  description = "Access key id for accessing s3."
  type = string
}

variable aws_secret_access_key {
  description = "Secret access key for accessing s3."
  type = string
}

provider "aws" {
  region = "us-east-2"
}

resource "aws_security_group" "algo_security_group" {
  name = "algo-security-group"
  ingress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "algobot" {
  ami = "ami-00399ec92321828f5"
  instance_type = "t2.micro"

  vpc_security_group_ids = [aws_security_group.algo_security_group.id]
  # the data is run under /var/lib/cloud/instances/${instance_id}.
  # The log is available in /var/log/cloud-init.log and /var/log/cloud-init-output.log
  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update
              sudo apt-get install -y awscli
              sudo apt-get install -y unzip
              sudo apt-get install -y python3-pip
              echo "Current Directory: $(pwd)"
              export AWS_ACCESS_KEY_ID=${var.aws_access_key_id}
              export AWS_SECRET_ACCESS_KEY=${var.aws_secret_access_key}
              aws s3 cp s3://algobot67/${var.zip_file_name} .
              unzip ${var.zip_file_name}
              python3 -m pip install -r requirements.txt
              nohup python3 main.py --token="${var.discord_bot_token}" &
              EOF
  tags = {
    Name = "Algobot main"
  }
}
