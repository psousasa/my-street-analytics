.PHONY: setup start


setup:
	@echo "# CREATING INFRASTRUCTURE WITH TERRAFORM..."
	cd terraform && terraform init && terraform apply && cd ..

	@echo "# BUILDING CONTAINERS..."
	docker build -f Dockerfile -t mystreetanalytics:latest .   


extract:
	@echo "# CREATING AND RUNNING CONTAINER..."
	docker run \
		-v $$GOOGLE_APPLICATION_CREDENTIALS:"/keys/gcp_key.json":ro \
		-e GOOGLE_APPLICATION_CREDENTIALS="/keys/gcp_key.json" \
		mystreetanalytics:latest

stop:
	@echo "# REMOVING CONTAINER IMAGE..."
	docker rmi -vf mystreetanalytics:latest

# only with terraform version >2.0
# @echo "# DESTROING INFRASTRUCTURE WITH TERRAFORM..."
# terraform && terraform destroy && cd ..


# transform:
# 	docker compose run dbt run