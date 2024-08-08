resource "aws_instance" "mlflow-server" {
  ami           = "ami-046d5130831576bbb"
  instance_type = "m5a.large" #can make variable
  key_name = var.shh-key-name
  depends_on = [ aws_key_pair.ec2-key, local_file.ssh-key ]

  security_groups = [aws_security_group.ec2_sg.name]
  iam_instance_profile = aws_iam_instance_profile.mlflow-instance-profile.id

  user_data = file("scripts/ec2-server.sh") #can make variable
  tags = {
    Name = "${var.project_id}" #need to adjust that to include a server name
  }
  root_block_device {
    volume_size = 20 # Size in GB
  }
  # provisioner "remote-exec"{
  #   inline = [
  #     "git clone https://github.com/Dakini/prima-diabetes-mlops.git",
  #     "cd prima-diabetes-mlops "

  #   ]

  #   connection {
  #     type        = "ssh"
  #     user        = "ec2-user"
  #     private_key = file("${var.shh-key-name}.pem") # Replace with the path to your private key
  #     host        = self.public_ip
  #   }
  # }

}


# RSA key of size 4096 bits
resource "tls_private_key" "rsa-4096-key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "ec2-key" {
    key_name = var.shh-key-name
    public_key = tls_private_key.rsa-4096-key.public_key_openssh
}

resource "local_file" "ssh-key" {
    filename = "${var.shh-key-name}.pem"
    content = tls_private_key.rsa-4096-key.private_key_openssh
    provisioner "local-exec" {
    command = "chmod 400 ${var.shh-key-name}.pem"
  }
}

resource "aws_security_group" "ec2_sg" {
    name = "Security group of the ec2 instance"
    description = "security group of the ec2 instance"
    vpc_id = "vpc-08794875ef25acc4c"
    ingress {
        description = "SSH"
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
        ipv6_cidr_blocks=["::/0"]
    }

    ingress {
      description = "Mlflow-server"
      from_port = 5001
      to_port = 5001
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      ipv6_cidr_blocks = ["::/0"]
    }

    ingress {
      description = "postgres"
      from_port = 5432
      to_port = 5432
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      ipv6_cidr_blocks = ["::/0"]
    }

    ingress {
      description = "mage"
      from_port = 6789
      to_port = 6789
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      ipv6_cidr_blocks = ["::/0"]
    }

    ingress {
      description = "grafana"
      from_port = 3000
      to_port = 3000
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      ipv6_cidr_blocks = ["::/0"]
    }

    egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

output "ip" {
  value = aws_instance.mlflow-server.public_ip
}
output "dns" {
  value = aws_instance.mlflow-server.public_dns
}
