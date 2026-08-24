terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
  zone    = var.zone
}

resource "google_storage_bucket" "semiconductor_data_lake" {
  name          = var.gcs_bucket_name
  location      = var.location
  storage_class             = var.gcs_storage_class
  force_destroy             = true
  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "semiconductor_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}
