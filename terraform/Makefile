tf-init:
	terraform init

tf-plan:
	terraform plan

tf-up:
	terraform apply

tf-down:
	terraform destroy

tf-config:
	terraform output

ssh-getkey:
	terraform output -raw private_key > private_key.pem && chmod 600 private_key.pem && cat private_key.pem
	
ssh-ec2:
	terraform output -raw private_key > private_key.pem && chmod 600 private_key.pem && ssh -o StrictHostKeyChecking=no -o IdentitiesOnly=yes -i private_key.pem ubuntu@$$(terraform output -raw ec2_public_dns) && rm private_key.pem	

listen-mysql:
	terraform output -raw private_key > private_key.pem && chmod 600 private_key.pem && ssh -i private_key.pem -v -N  -L localhost:3306:localhost:3306 -o ConnectTimeout=15 -o ServerAliveInterval=30 -o ServerAliveCountMax=3 ubuntu@$$(terraform output -raw ec2_public_dns) && rm private_key.pem	

listen-psql:
	terraform output -raw private_key > private_key.pem && chmod 600 private_key.pem && ssh -i private_key.pem -v -N  -L localhost:5432:localhost:5432 -o ConnectTimeout=15 -o ServerAliveInterval=30 -o ServerAliveCountMax=3 ubuntu@$$(terraform output -raw ec2_public_dns) && rm private_key.pem	
