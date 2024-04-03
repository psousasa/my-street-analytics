.PHONY: setup start


setup:
	@echo "# CREATING INFRASTRUCTURE WITH TERRAFORM..."
	cd terraform && terraform init && terraform apply && cd ..

	@echo "# BUILDING CONTAINERS..."
	docker compose build


start:
	@echo "# CREATING AND STARTING CONTAINERS..."
	docker compose up -d

stop:
	@echo "# REMOVING CONTAINER IMAGE..."
	docker compose down

extract:
	@echo "# EXTRACTING DATA FROM SOURCE..."
	docker compose run pyextract


# only with terraform version >2.0
# @echo "# DESTROING INFRASTRUCTURE WITH TERRAFORM..."
# terraform && terraform destroy && cd ..


# transform:
# 	docker compose run dbt run