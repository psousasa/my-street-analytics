
variable "GCP_BUCKET" {
}

variable "GCP_BUCKET_LOCATION" {
}

variable "GCP_REGION" {
}

variable "GCP_PROJECT" {
}

variable "GCP_BQ_DATASET" {
}


terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}


provider "google" {
# Credentials only needs to be set if you do not have the GOOGLE_APPLICATION_CREDENTIALS set
#  credentials = 
  project = var.GCP_PROJECT
  region  = var.GCP_REGION
}



resource "google_storage_bucket" "data-lake-bucket" {
  name          = var.GCP_BUCKET
  location      = var.GCP_BUCKET_LOCATION

  # Optional, but recommended settings:
  storage_class = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}


resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.GCP_BQ_DATASET
  project    = var.GCP_PROJECT
  location   = var.GCP_REGION
  
  # delete_contents_on_destroy = true # only with version >2.0
  
}
